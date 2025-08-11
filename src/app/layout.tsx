import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from '@/components/ThemeProvider';
import { ProgressProvider } from '@/components/ProgressProvider';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'felixforlearnai — AI Engineering from Scratch',
  description: '260+ lessons across 20 phases. Build neural networks, transformers, and LLMs from first principles. Python, TypeScript, Rust, Julia.',
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
