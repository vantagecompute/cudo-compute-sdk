import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import * as fs from 'fs';
import * as path from 'path';

// Function to read version from pyproject.toml
function getVersionFromPyproject(): string {
  try {
    const pyprojectPath = path.join(__dirname, '../pyproject.toml');
    const content = fs.readFileSync(pyprojectPath, 'utf8');
    
    // Extract version using regex
    const versionMatch = content.match(/^version\s*=\s*["']([^"']+)["']/m);
    
    if (versionMatch) {
      return versionMatch[1];
    }
    
    throw new Error('Version not found in pyproject.toml');
  } catch (error) {
    console.error('Error reading version from pyproject.toml:', error);
    return '0.0.0'; // fallback version
  }
}

const projectVersion = getVersionFromPyproject();

const config: Config = {
  title: 'Cudo Compute SDK',
  tagline: `Python SDK for Cudo Compute - v${projectVersion}`,
  favicon: 'img/favicon.ico',

  url: 'https://vantagecompute.github.io',
  baseUrl: '/cudo-compute-sdk/',

  organizationName: 'vantagecompute',
  projectName: 'cudo-compute-sdk',
  deploymentBranch: 'main',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  markdown: {
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn'
    }
  },
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    [
      'classic',
      {
        docs: {
          path: './docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/vantagecompute/cudo-compute-sdk/tree/main/docs/',
          sidebarCollapsible: true,
          sidebarCollapsed: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
  plugins: [
    [ 
      'docusaurus-plugin-llms',
      {
        // Options here
        generateLLMsTxt: true,
        generateLLMsFullTxt: true,
        docsDir: 'docs',
        ignoreFiles: ['advanced/*', 'private/*'],
        title: 'Cudo Compute SDK Documentation',
        description: 'Complete Python SDK documentation for Cudo Compute cloud platform.',
        includeBlog: false,
        // Content cleaning options
        excludeImports: true,
          removeDuplicateHeadings: true,
          // Generate individual markdown files following llmstxt.org specification
          generateMarkdownFiles: true,
          // Control documentation order
          includeOrder: [],
          includeUnmatchedLast: true,
          // Path transformation options
          pathTransformation: {
            // Paths to ignore when constructing URLs (will be removed if found)
            ignorePaths: ['docs'],
            // Paths to add when constructing URLs (will be prepended if not already present)
            // addPaths: ['api'],
          },
          // Custom LLM files for specific documentation sections
          customLLMFiles: [
            {
              filename: 'llms-index.txt',
              includePatterns: ['docs/index.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Documentation Index',
              description: 'Index reference for Cudo Compute SDK'
            },
            {
              filename: 'llms-usage.txt',
              includePatterns: ['docs/usage.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Usage Documentation',
              description: 'Usage documentation and examples for Cudo Compute SDK'
            },
            {
              filename: 'llms-api-reference.txt',
              includePatterns: ['docs/api-reference.md'],
              fullContent: true,
              title: 'Cudo Compute SDK API Reference',
              description: 'Complete API reference for Cudo Compute SDK'
            },
            {
              filename: 'llms-contributing.txt',
              includePatterns: ['docs/contributing.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Contributing Guide',
              description: 'Contributing documentation for Cudo Compute SDK'
            },
            {
              filename: 'llms-installation.txt',
              includePatterns: ['docs/installation.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Installation Guide',
              description: 'Installation documentation for Cudo Compute SDK'
            },
            {
              filename: 'llms-architecture.txt',
              includePatterns: ['docs/architecture.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Architecture',
              description: 'Architecture documentation for Cudo Compute SDK'
            },
            {
              filename: 'llms-contact.txt',
              includePatterns: ['docs/contact.md'],
              fullContent: true,
              title: 'Cudo Compute SDK Contact Information',
              description: 'Contact documentation for Cudo Compute SDK'
            },
          ],
        },
    ],
  ],

  customFields: {
    projectVersion: projectVersion,
  },

  themeConfig: {
    navbar: {
      title: `Cudo Compute SDK Documentation v${projectVersion}`,
      logo: {
        alt: 'Vantage Compute Logo',
        src: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        srcDark: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        href: 'https://vantagecompute.github.io/cudo-compute-sdk/',
        target: '_self',
      },
      items: [
        {
          href: 'https://pypi.org/project/cudo-compute-sdk/',
          label: 'PyPI',
          position: 'right',
          className: 'pypi-button',
        },
        {
          href: 'https://github.com/vantagecompute/cudo-compute-sdk',
          label: 'GitHub',
          position: 'right',
          className: 'github-button',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Vantage Compute Logo',
        src: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        href: 'https://vantagecompute.ai',
      },
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Installation',
              to: '/installation',
            },
            {
              label: 'Usage Examples',
              to: '/usage',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/vantagecompute/cudo-compute-sdk/discussions',
            },
            {
              label: 'Issues',
              href: 'https://github.com/vantagecompute/cudo-compute-sdk/issues',
            },
            {
              label: 'Support',
              href: 'https://vantagecompute.ai/support',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/vantagecompute/cudo-compute-sdk',
            },
            {
              label: 'Vantage Compute',
              href: 'https://vantagecompute.ai',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/cudo-compute-sdk/',
            },
          ],
        },
      ],
      copyright: 'Copyright &copy; ' + new Date().getFullYear() + ' Vantage Compute.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['shell-session', 'python', 'bash'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 5,
    },
  },
};

export default config;
