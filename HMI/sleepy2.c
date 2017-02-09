

/** compile using gcc -o demo demo.c `mysql_config --cflags --libs` **/

#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/mman.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>
#include "sleepy.h"


#define MY_PASS "helicopterinho"
#define BUF_MAX 1000000

#define GANHO_ADC 3/4096
#define DRIVER 1
#define BANCODADOS 0
void finish_with_error();
void data_treatment();

unsigned int RXbuf[BUF_MAX];
unsigned int buf_dados[BUF_MAX][7];
unsigned int num_points;
float dados_tratados[BUF_MAX][7];


void data_treatment(void)
{
	int i, k, bef=0, cur=0, count=0, sub, v_i[200]={0};

	for(i=0;i<num_points;i++)
	{
				bef = cur;
				cur = buf_dados[i][0];
				if(cur - bef < 0)
				{
					v_i[count] = i;
					count++;
				}
	}
	if(count > 0)
	{
		for(k=0;k<count;k++)
		{
			for(i=v_i[k]; i<num_points; i++)
			{
				buf_dados[i][0] += 65535;
			}

		}
	}

	sub = buf_dados[0][0];

	for(i=0;i<num_points;i++)
	{
		buf_dados[i][0] -= sub;
		dados_tratados[i][0] = (float) buf_dados[i][0];
		dados_tratados[i][4] = (float) (buf_dados[i][4]*0.00073242 - 1.5)*1000/15;//
		dados_tratados[i][2] = (float) (buf_dados[i][2]*0.00073242 - 1.5)*1000/15;//
		dados_tratados[i][1] = (float) (buf_dados[i][1]*0.00073242 - 1.5)*1000/15;
		dados_tratados[i][3] = (float) (buf_dados[i][3]*0.00073242 - 1.5)*1000/15;
		dados_tratados[i][5] = (float) (buf_dados[i][5]*0.00073242 - 1.5)*15300/33;
		dados_tratados[i][6] = (float) (buf_dados[i][6]*0.00073242 - 1.5)*1000/15;


	}

}

int mysleep(long miliseconds)
{
   struct timespec req, rem;

   if(miliseconds > 999)
   {
        req.tv_sec = (int)(miliseconds / 1000);                            /* Must be Non-Negative */
        req.tv_nsec = (miliseconds - ((long)req.tv_sec * 1000)) * 1000000; /* Must be in range of 0 to 999999999 */
   }
   else
   {
        req.tv_sec = 0;                         /* Must be Non-Negative */
        req.tv_nsec = miliseconds * 1000000;    /* Must be in range of 0 to 999999999 */
   }
   return nanosleep(&req , &rem);
}

int main(int argc, char *argv[])
{
	char *query_usuario = NULL, *query_ensaio = NULL, *query_dados = NULL;
	int fd, i, numbytes, j=0, k=0, l=0, m=0, n=0, o=0, p=0, sleepy;
	unsigned int mytime = atoi(argv[1]);
	unsigned int time_min = atoi(argv[2]);
	unsigned int time_seg = atoi(argv[3]);
	unsigned int time_mseg = atoi(argv[4]);
	unsigned long totaltime=0, halftime=0;


	FILE *fp;
	/// Open the file to save the RX buffer
	fp = fopen("resultado.csv","w");


	printf("Ensaio de %d min %d s %d mseg em andamento...\n",time_min, time_seg, time_mseg);
	totaltime = time_min*60000 + time_seg*1000 + time_mseg;
	halftime = totaltime/2 - mytime;
	//printf("%d %d\n",totaltime,halftime);

	sleepy = mysleep(halftime);

	printf("Afundamento de %d ms em andamento...\n",mytime);
	mytime = mytime*1.5;
#if (DRIVER)

	printf("Mytime: %d\n",mytime);
	fd = open("/dev/bcm2835_spi", O_RDWR | O_SYNC);
	if (fd < 0)
	{
		fputs("open() failed, aborting...\n", stderr);
		return 255;
	}

	/// Write down to the driver the acquiring time
	if(write(fd,&mytime,sizeof(mytime))<0)
		fputs("write() failed\n",stderr);



	/// Read the results from the driver
	numbytes = read(fd, RXbuf, sizeof(RXbuf));
	if (numbytes < 0)
		fputs("read() failed for t1\n", stderr);

	printf("Termino do afundamento, tratamento de dados em andamento...\n");
	/// Write down the results in the destination file
#endif
	num_points = (mytime*1000)/100;
	j = num_points;
	l = 2*num_points;
	m = 3*num_points;
	n = 4*num_points;
	o = 5*num_points;
	p = 6*num_points;

	for(i=0;i<num_points;i++)
	{
		buf_dados[i][0] = RXbuf[i];
		buf_dados[i][1] = RXbuf[j];
		buf_dados[i][2] = RXbuf[l];
		buf_dados[i][3] = RXbuf[m];
		buf_dados[i][4] = RXbuf[n];
		buf_dados[i][5] = RXbuf[o];
		buf_dados[i][6] = RXbuf[p];
		j++; m++; n++; l++; o++; p++;

	}
	data_treatment();
	for(i=0; i<num_points; i++)
	{
		for(j=0; j<7; j++)
		{
			if (j==6)
			{
				fprintf(fp,"%.2f\n",dados_tratados[i][j]);
			}
			else
			{
				fprintf(fp,"%.2f\t",dados_tratados[i][j]);
			}

		}
	}


	fclose(fp);
	close(fd);

	free(query_usuario);
	free(query_dados);
	free(query_ensaio);

	query_usuario = NULL;
	query_ensaio = NULL;
	query_dados = NULL;

	printf("Dados tratados e inseridos no banco!\n########-C->Python-########\n");

	return 0;
}
