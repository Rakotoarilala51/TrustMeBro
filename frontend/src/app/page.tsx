"use client";
import { FaRobot } from "react-icons/fa";
export default function Home() {
  return (
    <div className="flex flex-col space-y-2">
        <div className="space-x-2 flex items-center justify-center">
          <select name="Catégorie" id="" className="bg-white p-1 w-54 rounded-sm h-8">
            <option value="Sport">Sport</option>
            <option value="Tech"> Tech</option>
            <option value="Politic">Politic</option>
          </select>
          <button className="bg-black p-1 rounded-lg text-white font-bold">Get News</button>
        </div>
        <div className=" flex items-center justify-center">
        <div className="bg-white w-180 h-50 rounded-lg">
            
        </div>
        </div>

        <div className="ml-72">
          <h3 className="font-bold text-sm">Read More:</h3>
        </div>
    </div>
  )
}
