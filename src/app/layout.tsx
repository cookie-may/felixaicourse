import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from '@/components/ThemeProvider';
import { ProgressProvider } from '@/components/ProgressProvider';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'SLAFAI - AI Engineering from Scratch',
  description: '260+ lessons across 20 phases. Build neural networks, transformers, and LLMs from first principles.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col">
        <ThemeProvider>
          <ProgressProvider>
            <Header />
            <main className="flex-1 pt-16">
              {children}
            </main>
            <Footer />
          </ProgressProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
