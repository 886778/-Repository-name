import type { Metadata } from 'next';
import type { ReactNode } from 'react';

import './styles.css';

export const metadata: Metadata = {
  title: 'AI 八字命理分析平台',
  description: '传统文化分析与自我反思工具',
};

export default function RootLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="zh-CN" dir="ltr">
      <body>{children}</body>
    </html>
  );
}
