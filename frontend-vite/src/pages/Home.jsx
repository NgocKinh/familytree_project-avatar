import React from "react";
import { useFamilyConfig } from "../context/FamilyConfigContext";

function Home() {
  const familyConfig = useFamilyConfig();

  return (
    <div
      className="min-h-[calc(100vh-64px)] w-full bg-cover bg-center bg-no-repeat flex flex-col items-center justify-center text-center px-4 py-8 sm:px-6 md:py-12"
      style={{
        backgroundImage: `url("${familyConfig.backgroundImage}")`,
      }}
    >
      <h1 className="font-sans text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight font-bold text-red-600 drop-shadow-[2px_2px_0_#2563eb] mb-2">
        {familyConfig.signboard}
      </h1>

      <div className="mb-4 md:mb-6">
        <h2 className="font-dancing text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-red-700 drop-shadow-[2px_2px_0_#fbbf24]">
          {familyConfig.subtitle}
        </h2>
      </div>

      <p className="text-xl sm:text-2xl md:text-3xl lg:text-4xl text-green-700 font-bold mb-2 md:mb-3 drop-shadow-lg">
        {familyConfig.sloganLines.map((line) => (
          <span key={line} className="block">
            {line}
          </span>
        ))}
      </p>

      <p className="whitespace-nowrap text-base sm:text-xl md:text-2xl lg:text-4xl text-blue-700 font-semibold mb-6 md:mb-10 drop-shadow-lg">
        {familyConfig.originLine}
      </p>

      <div className="w-full max-w-3xl rounded-2xl bg-black/50 px-4 py-4 sm:px-6 md:px-8 md:py-5 text-base sm:text-lg md:text-xl font-medium leading-relaxed text-yellow-100 shadow-lg">
        🌿 <b>{familyConfig.welcomeTitle}</b> — {familyConfig.welcomeText}
        <br />
        💡 Hãy sử dụng <b>nút Menu</b> để xem danh sách thành viên,
        cây gia phả hoặc những thông tin mới.
      </div>

      <p className="mt-4 w-full max-w-3xl rounded-xl bg-blue-900/75 px-4 py-3 text-sm leading-relaxed text-white shadow-lg xl:hidden">
        📱 Khi mở bằng Zalo, màn hình có thể không xoay. Hãy mở FamilyTree
        bằng Chrome và xoay ngang điện thoại để xem cây gia phả rõ hơn.
      </p>
    </div>
  );
}

export default Home;