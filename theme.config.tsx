import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span>FluentQA-Python</span>,
  project: {
    link: 'https://github.com/fluent-qa/daily-python.git',
  },
  chat: {
    link: 'https://github.com/fluent-qa',
  },
  docsRepositoryBase: 'https://github.com/fluent-qa/daily-python.git',
  footer: {
    text: 'Software QA Daily Python',
  },
}

export default config