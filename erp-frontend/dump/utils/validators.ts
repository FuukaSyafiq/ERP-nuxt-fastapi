/**
 * Validasi email
 */
export const isValidEmail = (email: string): boolean => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/**
 * Validasi nomor telepon Indonesia
 */
export const isValidPhone = (phone: string): boolean => {
  const regex = /^(\+62|62|0)8[1-9][0-9]{6,10}$/
  return regex.test(phone.replace(/\s/g, ''))
}

/**
 * Validasi password (min 8 karakter, huruf dan angka)
 */
export const isValidPassword = (password: string): boolean => {
  return password.length >= 8 && /[a-zA-Z]/.test(password) && /[0-9]/.test(password)
}

/**
 * Validasi tidak kosong
 */
export const isRequired = (value: string): boolean => {
  return value.trim().length > 0
}

/**
 * Validasi panjang minimum
 */
export const minLength = (value: string, min: number): boolean => {
  return value.length >= min
}

/**
 * Validasi panjang maksimum
 */
export const maxLength = (value: string, max: number): boolean => {
  return value.length <= max
}

