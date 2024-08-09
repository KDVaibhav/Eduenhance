import React from "react";
import {
  ChartBarIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
  TruckIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/solid";

const DashboardCard = ({ title, value, icon, color }) => (
  <div
    className={`bg-white rounded-lg shadow-md p-6 flex items-center ${color}`}
  >
    <div className="mr-4">{icon}</div>
    <div>
      <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  </div>
);

const Dashboard = () => {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <DashboardCard
          title="Total Revenue"
          value="$254,321"
          icon={<CurrencyDollarIcon className="h-8 w-8 text-green-500" />}
          color="text-green-500"
        />
        <DashboardCard
          title="New Orders"
          value="75"
          icon={<ClipboardDocumentListIcon className="h-8 w-8 text-blue-500" />}
          color="text-blue-500"
        />
        <DashboardCard
          title="Active Users"
          value="1,234"
          icon={<UserGroupIcon className="h-8 w-8 text-purple-500" />}
          color="text-purple-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Sales Overview
          </h2>
          {/* Add your chart component here */}
          <div className="h-64 bg-gray-200 flex items-center justify-center">
            <ChartBarIcon className="h-16 w-16 text-gray-400" />
            <span className="ml-2 text-gray-600">Chart Placeholder</span>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Recent Activities
          </h2>
          <ul className="space-y-4">
            <li className="flex items-center text-gray-600">
              <TruckIcon className="h-5 w-5 mr-2" /> Order #1234 shipped
            </li>
            <li className="flex items-center text-gray-600">
              <UserGroupIcon className="h-5 w-5 mr-2" /> New customer registered
            </li>
            <li className="flex items-center text-gray-600">
              <Cog6ToothIcon className="h-5 w-5 mr-2" /> System update completed
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-300">
            Create Order
          </button>
          <button className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-300">
            Add Product
          </button>
          <button className="bg-purple-500 text-white py-2 px-4 rounded hover:bg-purple-600 transition duration-300">
            Manage Users
          </button>
          <button className="bg-yellow-500 text-white py-2 px-4 rounded hover:bg-yellow-600 transition duration-300">
            Generate Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
