import { getMessage } from '@ai-bazi/i18n';

export default function Home() {
  return (
    <main>
      <section aria-labelledby="page-title">
        <p className="eyebrow">M0 Repository Bootstrap</p>
        <h1 id="page-title">{getMessage('zh-CN', 'productName')}</h1>
        <p>{getMessage('zh-CN', 'bootstrapReady')}</p>
        <p className="notice">{getMessage('zh-CN', 'scopeNotice')}</p>
      </section>
    </main>
  );
}
