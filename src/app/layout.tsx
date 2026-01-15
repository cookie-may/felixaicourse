import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from '@/components/ThemeProvider';
import { ProgressProvider } from '@/components/ProgressProvider';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'Felix | AI Engineering Learning Platform',
  description: '20 phases from math foundations to autonomous agent swarms. 272+ lessons. Learn AI with AI, then build and ship real tools.',
  keywords: ['AI', 'Machine Learning', 'Deep Learning', 'LLM', 'Transformers', 'Agent Engineering', 'Learn by Building'],
  authors: [{ name: 'Felix Learning', url: 'https://felixforlearnai.com' }],
  creator: 'Felix Learning',
  publisher: 'Felix Learning',
  icons: { icon: '/logo.png', apple: '/logo.png' },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="dark" suppressHydrationWarning>
      <body style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <ThemeProvider>
          <ProgressProvider>
            <Header />
            <main style={{ flex: 1 }}>
              {children}
            </main>
            <Footer />
          </ProgressProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
