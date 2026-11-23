/**
 * La API envía dinero como string decimal ("1234.50").
 * Aquí solo se FORMATEA; no se hace aritmética monetaria en el frontend.
 */
export function formatMoney(amount: string, currency = "MXN"): string {
  return new Intl.NumberFormat("es-MX", { style: "currency", currency }).format(Number(amount));
}
