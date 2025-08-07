"use client";
import { useState } from "react";
import { FaRobot, FaPlay, FaSoundcloud } from "react-icons/fa";
export default function Home() {
  const [summary, setSummary] = useState<string>("");
  return (
    <div className="flex flex-col space-y-2">
        <form action="" className="space-x-2 flex items-center justify-center">
          <select
            name="category"
            id=""
            className="bg-white p-1 w-54 rounded-sm h-8"
          >
            <option value="Sport">Sport</option>
            <option value="Tech"> Tech</option>
            <option value="Politic">Politic</option>
            <option value="Education">Education</option>
          </select>
          <button className="bg-black p-1 rounded-lg text-white font-bold">
            Get News
          </button>
        </form>
   
      <div className=" flex items-center justify-center">
        <div className="bg-white w-180 h-50 rounded-lg">{summary}</div>
      </div>
      <div className="flex items-end justify-end mr-82">
        <div className="bg-black w-7 h-7 flex items-center justify-center rounded-full">
        <FaPlay className="text-white ml-1"/>
        </div>
      </div>
      <div className="ml-72">
        <h3 className="font-bold text-sm">Source:</h3>
      </div>
    </div>
  );
}
