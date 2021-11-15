// dll_for_py.cpp : Defines the exported functions for the DLL application.
//
#include "stdafx.h"


// test.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

#include"m_RK3_1.h"

using namespace std;


extern "C" __declspec(dllexport) void __stdcall work_RK31R(double** data, double * start, int * gran, int* _i)
{

	*_i = m_RK3_1_r(start, gran, "test2.txt", data);

}

extern "C" __declspec(dllexport) void __stdcall del_mem(double** data)
{
	delete[](*data);
	//cout << "- mem" << endl;
}