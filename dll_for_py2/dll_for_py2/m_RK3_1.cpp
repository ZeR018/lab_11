#include"pch.h"
#include"m_RK3_1.h"
#include"fun.h"
#include<fstream>


//������ ������������� �������� ������, ������� ��� �������� � ������ ����� ���� �������� ��������
//�������� ����� ���������� � v1 �������� �������(�� ���� 2-� �� �����) ���� �������� perem[__v1]
//																��� ����������� perem[1]						
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
	k1[0] = f1_11(x, v1, v2, start_p[__k], start_p[__f], start_p[__m]);
	k2[0] = f2_11(x, v1, v2, start_p[__k], start_p[__f], start_p[__m]);

	k1[1] = f1_11(x + h / 2, v1 + h / 2 * k1[0], v2 + h / 2 * k2[0], start_p[__k], start_p[__f], start_p[__m]);
	k2[1] = f2_11(x + h / 2, v1 + h / 2 * k1[0], v2 + h / 2 * k2[0], start_p[__k], start_p[__f], start_p[__m]);

	k1[2] = f1_11(x + h / 2, v1 + h / 2 * k1[1], v2 + h / 2 * k2[1], start_p[__k], start_p[__f], start_p[__m]);
	k2[2] = f2_11(x + h / 2, v1 + h / 2 * k1[1], v2 + h / 2 * k2[1], start_p[__k], start_p[__f], start_p[__m]);

	k1[3] = f1_11(x + h, v1 + h * k1[2], v2 + h * k2[2], start_p[__k], start_p[__f], start_p[__m]);
	k2[3] = f2_11(x + h, v1 + h * k1[2], v2 + h * k2[2], start_p[__k], start_p[__f], start_p[__m]);

	v_value res;
	res.v1 = v1 + h / 6 * (k1[0] + 2 * k1[1] + 2 * k1[2] + k1[3]);
	res.v2 = v2 + h / 6 * (k2[0] + 2 * k2[1] + 2 * k2[2] + k2[3]);
	return res;
}

// �������� ������� ������ 9 � ����� perem[__x] ��� ��������� �������� u(x0)=u0
// �� ������ ������ �� ������������
double st_true_sol_ex_11(double *perem, double* start_p)
{
	double fmgk = (start_p[__f]  * start_p[__m] * G) / start_p[__k];
	//double c2 = 7.5 - fmgk;
	double c2 = start_p[__v01] - fmgk; // ������ ������ 7.5? �������� ������!!!!!!!! (������ ����� ������ ���� start_p[__v01])
	double sq = sqrt(start_p[__k] / start_p[__m]);

	return c2 * cos(sq * perem[__x]) + fmgk;
}


int m_RK3_1_r(double* start_p, int* gran, string name_txt, double** py)
{
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

	

	//������������� �������
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

	//���������� � ������ 1-� ��������
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
			std::cout << "1\n";
			break;
		}
	
	
		if (z)
		{
			perem[__h1] = perem[__h1] * 2;
			perem[__c2] += 1.0;
		}
	
		z = 0;
	
	
		//����������� x
		perem[__x] += perem[__h1];
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
	
		//���������� 
		
		// double x, double v1, double v2, double h, double* start_p, double* k1, double* k2
		temp1 = st_RK4_11(perem[__x], perem[__v01], perem[__v02], perem[__h1], start_p, k1, k2);
		temp2 = st_RK4_11(perem[__x], perem[__v01], perem[__v02], perem[__h1] / 2, start_p, k1, k2);
		temp2 = st_RK4_11(perem[__x] + perem[__h1] / 2, temp2.v1, temp2.v2, perem[__h1] / 2, start_p, k1, k2);
	
		//��������� S---------------------------
		s_temp = fabs((temp1.v1 - temp2.v1) / (pow(2, P) - 1) );
		
		if (gran[__contr_e]) //c ���������� ���� ��� ���
		{
			//�������, ���� ��� ������� ����� �� ���� ���������
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

			}
		}
	
		perem[__u1] = st_true_sol_ex_11(perem, start_p);
		perem[__E] = fabs(perem[__u1] - perem[__v1]);
	
		//----------------------------------------------------------------------
	
		//������ �������� � �����������
	
		perem[__v1] = temp1.v1;
		perem[__v2] = temp1.v2;
		perem[__s] = s_temp*pow(2, P);
	
		//������ � ������ �� ��� �����
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

	//�������� ������ � ������ � �����
	*py = new double[d_v.size()];
	std::memcpy(*py, d_v.data(), d_v.size() * sizeof d_v[0]);
	int size = d_v.size();

	d_v.~vector();
	
	delete[] perem;

	//������ � ����
	record(&_f, *py, size);
	//���������� ������ ������� 
	std::cout << "1";
	return size;
}
