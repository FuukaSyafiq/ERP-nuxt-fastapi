//dummy
import { reactive, ref, computed } from "vue";

export function usePasswordSettings() {
  const form = reactive({
    email: "",
    currentPassword: "",
    newPassword: "",
  });

  const isSaving = ref(false);
  const message = ref("");
  const success = ref<boolean | null>(null);

  const messageClass = computed(() =>
    success.value === null
      ? ""
      : success.value
      ? "text-emerald-400"
      : "text-red-400"
  );

  const validate = () => {
    if (!form.currentPassword || !form.newPassword) {
      return "Semua field sandi wajib diisi.";
    }
    if (form.newPassword.length < 8) {
      return "Kata sandi baru minimal 8 karakter.";
    }
    if (form.currentPassword == form.newPassword) {
      return "Kata sandi sekarang dan yang baru masih sama";
    }
  };

  const changePassword = async () => {
    isSaving.value = true;
    message.value = "";
    success.value = null;

    const err = validate();
    if (err) {
      success.value = false;
      message.value = err;
      isSaving.value = false;
      return;
    }
    const api = useApi();
    try {
      const token = useCookie("auth_token", { path: "/" });
      console.log(`tes ${token.value}`);
      const response = await api.post<{ message: string }>(
        `/auth/forgot-password`,
        {
          email: form.email,
          oldPassword: form.currentPassword,
          newPassword: form.newPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );

      success.value = true;
      message.value = response.message;
      form.currentPassword = "";
      form.newPassword = "";
    } catch (err: any) {
      if (err.status === 401) {
        // Unauthorized
        success.value = false;
        message.value = "Password lama salah";
      } else {
        success.value = false;
        message.value = err.data?.error || "Gagal mengubah password";
      }
    } finally {
      isSaving.value = false;
    }
  };

  return {
    form,
    isSaving,
    message,
    messageClass,
    changePassword,
    onSubmit: changePassword,
  };
}
