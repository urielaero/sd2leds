/*----------------------------------------------------------------------*/
/* FatFs sample project for generic microcontrollers (C)ChaN, 2012      */
/*----------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include "ff.h"
#include "spidev_test.h"

FATFS Fatfs;		/* File system object */
FIL Fil;			/* File object */
//char Buff[128];		/* File read buffer */


void die (		/* Stop with dying message */
	FRESULT rc	/* FatFs return value */
)
{
	f_unmount(NULL,"",0,0);
	printf("0\n");
	exit(0);
}

int main (void)
{
	char Buff[128];
	FRESULT rc;				/* Result code */
	DIR dir;				/* Directory object */
	FILINFO fno;			/* File information object */
	UINT bw, br, i;

	int isSdAccess = checkDevice();
	if(!isSdAccess){
		printf("0\n");
		return 0;
	}

	rc = f_mount(&Fatfs,"",1);		/* Register volume work area (never fails) */
	if (rc) die(rc);

//#if 1

	rc = f_open(&Fil, "MESSAGE.TXT", FA_READ);
	if (rc) die(rc);

	int countT = 0;
	for (;;) {
		rc = f_read(&Fil, Buff, sizeof Buff, &br);	
		if (rc || !br) break;
		countT++;
		for (i = 0; i < br; i++)		
			putchar(Buff[i]);
	}
	if (rc) die(rc);
	rc = f_close(&Fil);
	if (rc) die(rc);
	
	/*
#endif
#if 1
	
	printf("\nCreate a new file (hello.txt).\n");
	rc = f_open(&Fil, "HELLO.TXT", FA_WRITE | FA_CREATE_ALWAYS);
	if (rc) die(rc);

	printf("\nWrite a text data. (Hello world!)\n");
	rc = f_write(&Fil, "Hello world!\r\n", 14, &bw);
	if (rc) die(rc);
	printf("%u bytes written.\n", bw);

	printf("\nClose the file.\n");
	rc = f_close(&Fil);
	if (rc) die(rc);

#endif

	printf("\nOpen root directory.\n");
	rc = f_opendir(&dir, "");
	if (rc) die(rc);

	printf("\nDirectory listing...\n");
	for (;;) {
		rc = f_readdir(&dir, &fno);		
		if (rc || !fno.fname[0]) break;	
		if (fno.fattrib & AM_DIR)
			printf("   <dir>  %s\n", fno.fname);
		else
			printf("%8lu  %s\n", fno.fsize, fno.fname);
	}
	
	rc = f_closedir(&dir);
	if (rc) die(rc);
	*/	
	

	rc = f_unmount(NULL,"",0,0);
	//if (rc) die(rc);
	return 0;
}



/*---------------------------------------------------------*/
/* User Provided Timer Function for FatFs module           */
/*---------------------------------------------------------*/

DWORD get_fattime (void)
{
	return	  ((DWORD)(2012 - 1980) << 25)	/* Year = 2012 */
			| ((DWORD)1 << 21)				/* Month = 1 */
			| ((DWORD)1 << 16)				/* Day_m = 1*/
			| ((DWORD)0 << 11)				/* Hour = 0 */
			| ((DWORD)0 << 5)				/* Min = 0 */
			| ((DWORD)0 >> 1);				/* Sec = 0 */
}

