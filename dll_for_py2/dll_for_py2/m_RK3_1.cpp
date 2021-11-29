#include"pch.h"
#include"m_RK3_1.h"
#include"fun.h"
#include<fstream>


//данные предоставляют сплошной массив, поэтому для удобства я сделал набор типо понятных символов
//например чтобы обратиться к v1 элементу массива(по сути 2-й по счету) надо написать perem[__v1]
//																что равносильно perem[1]						
enum { __x,__v1,__v2, __s, __h1, __h2, __h3,__u1,__u2, __E,__c1,__c2 };
enum {__x0,__v01,__v02,__h0,__k,__f,__m,__e,__max_step, __gran, __toch};
enum {_xu, __contr_e};

#define EPS 0.01
#define P 4
#define P_SIZE 12
#define G 10

struct v_value {
	double v1;
	double v2;
};

v_value st_RK4_11(double x, double v1, double v2, double h, double* start_p, double* k1, double* k2)
{
	k1[0] = f1_11(v2);
	k2[0] = f2_11(v1, start_p[__k], start_p[__f], start_p[__m]);

	k1[1] = f1_11(v2 + h * k1[0] / 2);
	k2[1] = f2_11(v1 + h * k2[0] / 2, start_p[__k], start_p[__f], start_p[__m]);

	k1[2] = f1_11(v2 + h * k1[1] / 2);
	k2[2] = f2_11(v1 + h * k2[1] / 2, start_p[__k], start_p[__f], start_p[__m]);

	k1[3] = f1_11(v2 + h * k1[2]);
	k2[3] = f2_11(v1 + h * k2[2], start_p[__k], start_p[__f], start_p[__m]);

	v_value res;
	res.v1 = v1 + h * (k1[0] + 2 * k1[1] + 2 * k1[2] + k1[3]) / 6;
	res.v2 = v2 + h * (k2[0] + 2 * k2[1] + 2 * k2[2] + k2[3]) / 6;
	return res;
}

// Истинное решение задачи 9 в точке perem[__x] при начальных условиях u(x0)=u0
// На данный момент не используется
v_value st_true_sol_ex_11(double *perem, double* start_p)
{
	double fmgk = (start_p[__f]  * start_p[__m] * G) / start_p[__k];
	//double c2 = 7.5 - fmgk;
	double sq = sqrt(start_p[__k] / start_p[__m]);

	double x0 = start_p[__x0] * sq;
	double x1 = perem[__x];
	double u0 = start_p[__v01];
	double u1 = start_p[__v02];


	double c2 = (u0 - u1*sin(x0)-fmgk)/(cos(x0)+sin(x0)*sin(x0)*sq);

	v_value pr;
	if (sin(x0) != 0)
	{
		double c1 = (u0 - fmgk - c2) / sin(x0);
		pr.v1 =  c1*sin(sq*x1)+c2*cos(sq*x1)+fmgk;
		pr.v2 = c1 * cos(x1 * sq) * sq - c2 * sin(x1 * sq) * sq;
	}
	else
	{
		pr.v1 = c2 * cos(sq * x1) + fmgk;
		pr.v2 = c2 * sin(x1 * sq) * sq;
	}

	return pr;
}



int m_RK3_1_r(double* start_p, int* gran, string name_txt, double** py)
{

	//start_p[__k] = start_p[__k] * 100;
	//start_p[__v01] = start_p[__v01] * 0.01;

	double v_temp = 0.0;
	double s_temp = 0.0;
	double v2 = 0.0;
	//------------------x---v1---e---h
	double* perem = new double[P_SIZE];
	double k1[4] = {};
	double k2[4] = {};
	int z = 0;
	double tmp = 0.0;
	vector<double> d_v;

	string name = string(name_txt);
	ofstream _f(name);

	

	//инициализация массива
	perem[__x] = start_p[__x0];
	perem[__v1] = start_p[__v01];
	perem[__v2] = start_p[__v02];
	perem[__s] = 0.0;
	perem[__h1] = start_p[__h0];
	perem[__h2] = 0.0;
	perem[__h3] = 0.0;
	perem[__u1] = start_p[__v01];
	perem[__u2] = start_p[__v02];
	perem[__E] = 0.0;
	perem[__c1] = 0.0;
	perem[__c2] = 0.0;

	//добавление в вектор 1-х значений
	d_v.push_back(perem[__x]);
	d_v.push_back(perem[__v1]);
	d_v.push_back(perem[__v2]);
	d_v.push_back(perem[__v1]);
	d_v.push_back(perem[__v2]);
	d_v.push_back(perem[__s]);
	d_v.push_back(perem[__h1]);
	d_v.push_back(perem[__u1]);
	d_v.push_back(perem[__u2]);
	d_v.push_back(perem[__E]);
	d_v.push_back(perem[__c1]);
	d_v.push_back(perem[__c2]);

	v_value temp1;
	v_value temp2;

	int j = 1;

	//perem[gran[0]] < start_p[__gran] && i < static_cast<int>(start_p[__max_step])
	for (int i = 0; ; i++)
	{
		if (i > static_cast<int>(start_p[__max_step]))
		{
			break;
		}
	
	
		/*if (z)
		{
			perem[__h1] = perem[__h1] * 2;
			perem[__c2] += 1.0;
			continue;
		}
	
		z = 0;*/
	
	
		//увеличиваем x
		
		//std::cout << perem[__x];

		//if (perem[__x] > 10)
		//	break;

		//gran x------------------------------------------------
		if (start_p[__gran] + start_p[__toch] < perem[__x])
		{
			perem[__x] -= perem[__h1];
			i--;
			j = 0;
			perem[__h1] /= 2;
			if (perem[__h1] < start_p[__toch])
			{
				break;
			}
			perem[__c1] += 1.0;
			continue;
		}
		//-----------------------------------------------------------
	
		//вычисление 
		
		// double x, double v1, double v2, double h, double* start_p, double* k1, double* k2
		temp1 = st_RK4_11(perem[__x], perem[__v01], perem[__v02], perem[__h1], start_p, k1, k2);

		temp2 = st_RK4_11(perem[__x], perem[__v01], perem[__v02], perem[__h1] / 2, start_p, k1, k2);
		temp2 = st_RK4_11(perem[__x] + perem[__h1] / 2, temp2.v1, temp2.v2, perem[__h1] / 2, start_p, k1, k2);
	
		//Вычисляем S---------------------------
		s_temp = fabs((temp1.v1 - temp2.v1) / (pow(2, P) - 1) );
		
		if (gran[__contr_e]) //c изминением шага или без
		{
			//условие, если рез функции зашел за наши параметры
			if (s_temp > start_p[__e])
			{
				i--;
				perem[__h1] = perem[__h1] / 2;
				perem[__c1] += 1.0;
				continue;
			}

			if (s_temp < start_p[__e] / pow(2, P + 1))
			{
				perem[__h1] = perem[__h1] * 2;
				perem[__c2] += 1.0;
				continue;
			}
		}

		perem[__x] += perem[__h1];
	
		v_value true_sol = st_true_sol_ex_11(perem, start_p);
		perem[__u1] = true_sol.v1;
		perem[__u2] = true_sol.v2;

		//perem[__u1] = st_true_sol_ex_11(perem, start_p);
		//perem[__E] = fabs(perem[__u1] - perem[__v1]);
	
		//----------------------------------------------------------------------
	
		//пихаем значения и погрешность
	
		perem[__v1] = temp1.v1;
		perem[__v2] = temp1.v2;
		perem[__s] = s_temp*pow(2, P);
	
		//кидаем в вектор то что нужно
		d_v.push_back(perem[__x]);
		d_v.push_back(perem[__v1]);
		d_v.push_back(perem[__v2]);
		d_v.push_back(temp2.v1);
		d_v.push_back(temp2.v2);
		d_v.push_back(perem[__s]);
		d_v.push_back(perem[__h1]);
		d_v.push_back(perem[__u1]);
		d_v.push_back(perem[__u2]);
		d_v.push_back(perem[__E]);
		d_v.push_back(perem[__c1]);
		d_v.push_back(perem[__c2]);
	
		perem[__c1] = 0.0;
		perem[__c2] = 0.0;
		
	}

	//собираем массив и кидаем в питон
	*py = new double[d_v.size()];
	std::memcpy(*py, d_v.data(), d_v.size() * sizeof d_v[0]);
	int size = d_v.size();

	d_v.~vector();
	
	delete[] perem;

	//запись в файл
	record(&_f, *py, size);
	//возвращаем размер массива 
	
	return size;
}
