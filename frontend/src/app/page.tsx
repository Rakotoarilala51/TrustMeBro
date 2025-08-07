"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import Card from "@/components/Card";
import { TbFileCv } from "react-icons/tb";
import { MdWorkOutline, MdRecordVoiceOver } from "react-icons/md";
import { cardProps} from "@/types";

const cardList:cardProps[]=[
  {
    icon:TbFileCv,
    title:"AI CV summary",
    description:"get a full cv breakpoint by ai"
  },
  {
    icon:MdWorkOutline,
    title:"Job Matching",
    description:"Check how much your skills match with a job offer"
  },
  {
    icon:MdRecordVoiceOver,
    title:"Interview Prep",
    description:"Prepare HR interview + a little bit of technical interview based on you cv"
  },
  {
    icon:MdRecordVoiceOver,
    title:"Interview Prep",
    description:"Prepare HR interview + a little bit of technical interview based on you cv"
  }
]
const contenairVarient = {
  hidden:{},
  visible:{
    transition:{
      staggerChildren: 0.3,
    }
  }
}
const cardVarient={
  hidden:{opacity:0, y: 30},
    visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};
export default function Home() {
  return (
    <div>
    </div>
  )
}
