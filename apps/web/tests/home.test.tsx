import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import Home from '../app/page';

describe('M0 home page', () => {
  it('identifies the repository bootstrap state', () => {
    render(<Home />);

    expect(
      screen.getByRole('heading', { name: 'AI 八字命理分析平台' }),
    ).toBeInTheDocument();
    expect(screen.getByText('M0 工程骨架已就绪')).toBeInTheDocument();
  });
});
