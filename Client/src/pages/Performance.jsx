import RankingCard from "@components/RankingCard";
import { ChartBar } from "@components/Statistics/ChartBar";
import React from "react";
import { extracurricularData, testScoresData, examScoresData } from "../data";
import { ChartPie } from "@components/Statistics/ChartPie";

const Performance = () => {
  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <div className="mid-heading text-2xl font-bold mb-4">Rankings</div>
      <div className="flex flex-wrap justify-between gap-4 bg-white p-4 rounded-lg shadow">
        <RankingCard name="ExamRank" rank="12" color="#F44771" dir="up" />
        <RankingCard name="TestRank" rank="12" color="#FF9A3E" dir="up" />
        <RankingCard name="ActivityRank" rank="12" color="#332A7C" dir="up" />
        <RankingCard name="ClassRank" rank="12" color="#269CB6" dir="up" />
      </div>
      <div className="mid-heading text-2xl font-bold mt-8 mb-4">Statistics</div>
      <div className="flex flex-wrap">
        <div className="w-full md:w-1/2 p-2">
          <ChartBar
            name="Test_Score"
            chartData={testScoresData}
            dataKey="score"
            className="w-full"
            barColor={4}
          />
        </div>
        <div className="w-full md:w-1/2 p-2">
          <ChartBar
            name="Extracurricular"
            chartData={extracurricularData}
            dataKey="activities"
            className="w-full"
            barColor={1}
          />
        </div>
      </div>
      <div className="w-full p-2">
        <ChartPie chartData={examScoresData} />
      </div>
    </div>
  );
};

export default Performance;
