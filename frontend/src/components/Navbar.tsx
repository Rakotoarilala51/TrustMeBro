"use client";
import Link from "next/link";
import Image from "next/image";
import {route} from "@/types"
const links:route[]=[
    {href:"/cvsummary", label:"CV Summary"},
    {href:"/ai-cv-matching", label:"AI CV Matching"},
    {href:"/interview-prep", label:"Interview preparation"},
    {href:"/job-searching", label:"Offer Searching"},
]
export default function Navbar(){

    return (
        <div className="w-full p-1 flex justify-center items-center">
            <Link href={"#"}>News Summary</Link>
        </div>
    );
}