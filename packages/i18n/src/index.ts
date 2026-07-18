import zhCN from '../messages/zh-CN.json';

export const supportedLocales = ['zh-CN'] as const;
export type SupportedLocale = (typeof supportedLocales)[number];
export type MessageKey = keyof typeof zhCN;

const messages: Record<SupportedLocale, typeof zhCN> = {
  'zh-CN': zhCN,
};

export function getMessage(locale: SupportedLocale, key: MessageKey): string {
  return messages[locale][key];
}

export function getTextDirection(locale: string): 'ltr' | 'rtl' {
  return locale.startsWith('ar') ? 'rtl' : 'ltr';
}
