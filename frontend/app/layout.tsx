import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CineMatch",
  description: "Cautare semantica de filme",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ro">
      <body>{children}</body>
    </html>
  );
}
