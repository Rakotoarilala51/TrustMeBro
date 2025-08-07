"use client";
import Link from "next/link";
import Image from "next/image";
import { route } from "@/types";
const links: route[] = [
  { href: "/news-summary", label: "News Summary" },
  { href: "/fact-checking", label: "Fact checking" },
];
export default function Navbar() {
  return (
    <div className="w-full p-1 flex justify-between">
      <div className="font-bold text-xl">TrustMeBro</div>
      <div className="space-x-2">
        {links.map((link, e) => (
          <Link href={link.href}>{link.label}</Link>
        ))}
      </div>
      <div></div>
    </div>
  );
}
