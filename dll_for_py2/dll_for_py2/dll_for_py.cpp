// dll_for_py.cpp : Defines the exported functions for the DLL application.
//



// test.cpp : Defines the exported functions for the DLL application.
//

#include "pch.h"
#include <string>
#include"m_RK3_1.h"

using namespace std;


extern "C" __declspec(dllexport) void __stdcall work_RK31R(double** data, double * start, int * gran, int* _i)
{
	string s = "test2.txt";
	*_i = m_RK3_1_r(start, gran, s, data);
	std::cout << "hi";
}

extern "C" __declspec(dllexport) void __stdcall del_mem(double** data)
{
	delete[](*data);
	//cout << "- mem" << endl;
}