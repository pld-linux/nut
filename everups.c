/* everups.c - support for Ever UPS models

   Copyright (C) 2003 Mikolaj Tutak <mtutak@eranet.pl>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
*/

#include "main.h"
#include <sys/ioctl.h>

#define DEFAULT_SERIALNUMBER	"Unknown"

#define BATT_DISCHARGED_VOLT	100.0 /* battery completly discharged */
#define BATT_MIN_OB_VOLTAGE	105.0 /* min. battery voltage for OB work - default */
#define BATT_MAX_OB_VOLTAGE	125.0 /* 100% charged battery - OB */
#define BATT_MAX_OFF_VOLT	134.0 /* 100% charged battery - OFF */
#define BATT_MAX_OL_VOLT	140.0 /* 100% charged battery - OL*/

#define EVER_SET_FLAGS	13
#define EVER_SET_SBTIME	28

#define EVER_GET_FLAGS	141
#define EVER_GET_MODEL	173
#define EVER_GET_STATUS	175
#define EVER_GET_BATTV	189
#define EVER_GET_LINEV	245

#define EVER_FRAME_INIT	208

#define EVER_FRAME_ACK	208
#define EVER_FRAME_NACK	209

#define EVER_FLAG_RESET		1 /* ??? */
#define EVER_FLAG_SELFTEST	2
#define EVER_FLAG_BEEPOFF	4
#define EVER_FLAG_POWEROFF	8
#define EVER_FLAG_SELFTESTFAIL	16 /* ??? */
#define EVER_FLAG_5		32
#define EVER_FLAG_6		64
#define EVER_FLAG_7		128


char *ever_serialnumber = DEFAULT_SERIALNUMBER;
unsigned char ever_upstype = 0;
unsigned char ever_debug = 0;
unsigned int batt_min_ob_voltage = BATT_MIN_OB_VOLTAGE;

/* used external variables */
extern int sddelay;          /* shutdown delay, set by "-d $delay" in main.c */
extern int do_forceshutdown; /* shutdown delay, set by "-k" in main.c */

int ever_initframe(int tries)
{
	int i;
	unsigned char buffer[2];

	for( i=0; i<tries ; i++ ) {
		upssendchar( EVER_FRAME_INIT );
		upsrecvchars( (char*)buffer, 1 );

		if( buffer[0] == EVER_FRAME_ACK )
			return 1;

		if( buffer[0] == EVER_FRAME_NACK )
			upsrecvchars( (char*)buffer, 2 );

		/* tcflush( upsfd, TCIOFLUSH ); */
		upsflushin(0, nut_debug_level, "");
		usleep( 250000 );
	};

	/* tcflush( upsfd, TCIOFLUSH ); */
	upsflushin(0, nut_debug_level, "");
	upslogx( LOG_INFO, "everups: ever_initframe() failed (%i tries)", tries );
	return 0;
}

int ever_initups()
{
	unsigned char tmp[2];

	if( !ever_initframe(5) )
		return 0;

	upssendchar( EVER_FRAME_INIT );
	upsrecvchars( (char*)tmp, 2 );
	usleep( 250000 );

	return 1;
}

int ever_getupstype()
{
	if( !ever_initframe(1) )
		return 0;

	upssendchar( EVER_GET_MODEL );
	upsrecvchars( (char*)&ever_upstype, 1 );
	return 1;
}

char *ever_getupsname()
{
        switch(ever_upstype)
        {
	        case 67: return "NET 500-DPC";
		case 68: return "NET 700-DPC";
	        case 69: return "NET 1000-DPC";
        	case 70: return "NET 1400-DPC";
	        case 71: return "NET 2200-DPC";

        	case 73: return "NET 700-DPC";
	        case 74: return "NET 1000-DPC";
	        case 75: return "NET 1400-DPC";
	        case 76: return "NET 500-DPC";

	        case 81: return "AP 450-PRO";
        	case 82: return "AP 650-PRO";

	        default: return "Unknown";
	}
}

void ever_change_flags(unsigned char set_flags, unsigned char reset_flags)
{
	unsigned char ups_flags;

	if ( !ever_initframe(2) )
		return;

	upssendchar( EVER_GET_FLAGS );
        upsrecvchars( (char*)&ups_flags, 1 );

	if ( !ever_initframe(1) )
		return;

	upssendchar( EVER_SET_FLAGS );
	upssendchar( (ups_flags|set_flags)&(~reset_flags) );
}

void ever_beepon(void)
{
	ever_change_flags( 0, EVER_FLAG_BEEPOFF|EVER_FLAG_POWEROFF );
}

void ever_beepoff(void)
{
	ever_change_flags( EVER_FLAG_BEEPOFF, EVER_FLAG_POWEROFF );
}

void ever_poweroff(int delay)
{
	if ( !ever_initframe(2) )
		return;

	upssendchar( EVER_SET_SBTIME );
	upssendchar( (char)((float)delay/1.28+0.5) );  /* (1*1.28) sec */

	ever_change_flags( EVER_FLAG_POWEROFF, 0 );
}

void ever_poweron(void)
{
	ever_change_flags( EVER_FLAG_RESET, EVER_FLAG_POWEROFF );
}

void ever_autotest(void)
{
	ever_change_flags( EVER_FLAG_SELFTEST, EVER_FLAG_SELFTESTFAIL|EVER_FLAG_POWEROFF );
}

/* registered instant commands */
void instcmd (int auxcmd, int dlen, char *data)
{
        switch (auxcmd) {
                case CMD_BTEST1:        /* start battery test */
                        ever_autotest();
                        break;
                case CMD_OFF:		/* power off load */
                        ever_poweroff(0);
                        break;
                case CMD_ON:		/* power on load */
                        ever_poweron();
                        break;
                default:
                        upslogx( LOG_ERR, "instcmd: unknown type 0x%04x\n", auxcmd );
        }
}

void setvar (int auxcmd, int dlen, char *data)
{
        switch (auxcmd) {
                case INFO_LOWXFER:
                        break;

                case INFO_HIGHXFER:
                        break;

		case INFO_AUDIBLEALRM:
                        upslogx( LOG_ERR, "setvar: unknown type %i\n", dlen );
			if( dlen == 3 && data[0]=='O' && data[1]=='F' && data[2]=='F' )
				ever_beepoff();
			else
				ever_beepon();
			break;

                default:
                        upslogx( LOG_ERR, "setvar: unknown type 0x%04x\n", auxcmd );
        }
}

void init_serial(void)
{
        int clr_bit = TIOCM_DTR | TIOCM_RTS;
        ioctl( upsfd, TIOCMBIC, &clr_bit );
}

void upsdrv_updateinfo(void)
{
	int		battery = 0;
	int		standby = 0;
	char		temp[VALSIZE];
	unsigned char	recBuf[2];
	unsigned char	ups_status;
	unsigned char 	ups_flags;
	unsigned int	accuVoltage;
	unsigned int	lineVoltage;
	double		batteryCharge;
	
	/****
	Line status
	175->UPS, UPS=HGFEDCBA
	A=1       - battery
	A=0 & C=1 - standby 
	****/

	if( !ever_initframe(2) )
		return;

	upssendchar( EVER_GET_STATUS );
	upsrecvchars( (char*)&ups_status, 1 );

	battery = ( (ups_status&5)==4 );
	standby = ( (ups_status&1)==1 );

	/****
	Read UPS flags
	****/

	if ( !ever_initframe(1) )
		return;

	upssendchar( EVER_GET_FLAGS );
	upsrecvchars( (char*)&ups_flags, 1 );

	/****
	Accumulator voltage value
	****/

	if( !ever_initframe(1) )
		return;

	upssendchar( EVER_GET_BATTV );
	upsrecvchars( (char*)recBuf, 1 );

	accuVoltage = 150*(recBuf[0])/255;

	/****
	Line voltage
	****/

	if( !ever_initframe(1) )
		return;

	upssendchar( EVER_GET_LINEV );
	upsrecvchars( (char*)recBuf, 2 );

	if ( ever_upstype > 72 && ever_upstype < 77)
		lineVoltage = 100*(recBuf[0]+256*recBuf[1])/352;
	else
		lineVoltage = 100*(recBuf[0]+256*recBuf[1])/372;

	/****
	Battery charge
	****/


	if( battery )
		batteryCharge = 100.0 * (accuVoltage - BATT_DISCHARGED_VOLT) / (BATT_MAX_OB_VOLTAGE - BATT_DISCHARGED_VOLT);
	else if( standby )
		batteryCharge = 100.0 * (accuVoltage - BATT_DISCHARGED_VOLT) / (BATT_MAX_OFF_VOLT - BATT_DISCHARGED_VOLT);
	else /* online */
		batteryCharge = 100.0 * (accuVoltage - BATT_DISCHARGED_VOLT) / (BATT_MAX_OL_VOLT - BATT_DISCHARGED_VOLT);

	if( batteryCharge > 100 )
		batteryCharge = 100;
	else if( batteryCharge < 0 )
		batteryCharge = 0;

	status_init();

	if( standby )
		status_set( "OFF" );
	else if( battery )
		status_set( "OB" );
	else
		status_set( "OL" );

	if( battery && accuVoltage <= batt_min_ob_voltage )
		status_set( "LB" );

	/***
	if( ups_flags&EVER_FLAG_POWEROFF )
		status_set( "OFFPEND" );
	***/

	if( ups_flags&EVER_FLAG_SELFTEST )
		status_set( "TESTPEND" );

	if( ups_flags&EVER_FLAG_SELFTESTFAIL )
		status_set( "TESTFAIL" );

	status_commit();

	snprintf( temp, VALSIZE, "%03u", lineVoltage );
	setinfo ( INFO_UTILITY, temp );

	snprintf( temp,VALSIZE, "%03.1f", (double)accuVoltage/10.0 );
	setinfo ( INFO_BATTVOLT, temp );

	snprintf( temp, VALSIZE, "%03.1f", batteryCharge );
	setinfo ( INFO_BATTPCT, temp );

	setinfo( INFO_AUDIBLEALRM, (ups_flags&EVER_FLAG_BEEPOFF)?"OFF":"ON" );

	setinfo( INFO_LOWXFER, "???" );
	setinfo( INFO_HIGHXFER, "???" );

	if( ever_debug > 0 ) {
		setinfo( INFO_COPYRIGHT, "STAT:%02X FLAG:%02X min OB: %2.1fV", (int)ups_status, (int)ups_flags, (double)batt_min_ob_voltage/10.0 );
	}


	writeinfo();
}

/* initialize UPS */
void upsdrv_initups(void)
{
        /* check serial number from arguments */
        if( getval("serialnumber") != NULL ) {
                ever_serialnumber = getval("serialnumber");
        };

        if( getval("minbattvolt") != NULL ) {
		int minbattvolt = (int)(atof(getval("minbattvolt"))*10);

		if( minbattvolt >= BATT_DISCHARGED_VOLT && minbattvolt <= BATT_MAX_OB_VOLTAGE )
			batt_min_ob_voltage = minbattvolt;
        };

        if( getval("debug") != NULL ) {
                ever_debug = atoi( getval("debug") );
        };

        upsdebugx( 1, "Values of arguments:" );
        upsdebugx( 1, " serial number: '%s'", ever_serialnumber );

	open_serial( device_path, B300 );
	init_serial();

	ever_initups();
	ever_getupstype();
}

void upsdrv_shutdown(void)
{
        if (do_forceshutdown == 1) {
                /* power down the attached load immediately */
                printf("Forced UPS shutdown triggered, do it...\n");
        } else {
                /* power down the attached load after the given delay */
                printf("UPS shutdown with '%d' seconds delay triggered, wait now...\n", sddelay);
                sleep(sddelay);
        };

	ever_poweroff(2); /* power off load after 2 sec */
}

/* display help */
void upsdrv_help(void)
{
}

/* display banner */
void upsdrv_banner(void)
{
	printf("Network UPS Tools - Ever UPS driver 0.02 (%s)\n\n", UPS_VERSION);
}

/* tell main how many entries we need */
int upsdrv_infomax(void)
{
        return 32;
}

/* initialize information */
void upsdrv_initinfo(void)
{
	/* write constant data for this model */
	addinfo( INFO_MFR, "Ever", 0, 0 );
	addinfo( INFO_MODEL, ever_getupsname(), 0, 0 );
	addinfo( INFO_SERIAL, ever_serialnumber, 0, 0 );

	/* add other things to monitor */
	addinfo( INFO_STATUS, "", 0, 0 );
	addinfo( INFO_UTILITY, "", 0, 0 );
	addinfo( INFO_BATTPCT, "", 0, 0 );
	addinfo( INFO_BATTVOLT, "", 0, 0 );

	/* now add the instant commands */
	addinfo( INFO_INSTCMD, "", 0, CMD_BTEST1 );
	addinfo( INFO_INSTCMD, "", 0, CMD_OFF );
	addinfo( INFO_INSTCMD, "", 0, CMD_ON );

	/* RW variables */
	addinfo( INFO_AUDIBLEALRM, "", FLAG_RW | FLAG_ENUM, 2 );
	addinfo( INFO_ENUM, "ON", 1, INFO_AUDIBLEALRM );
	addinfo( INFO_ENUM, "OFF", 0, INFO_AUDIBLEALRM );
	addinfo( INFO_LOWXFER, "", FLAG_RW | FLAG_STRING, 3 );
	addinfo( INFO_HIGHXFER, "", FLAG_RW | FLAG_STRING, 3 );

	/* display debug info as copyright */
	if( ever_debug > 0 ) {
		addinfo( INFO_COPYRIGHT, "", 0, 0 );
	}

        upsh.instcmd = instcmd;
	upsh.setvar = setvar;
}

/* list flags and values that you want to receive via -x */
void upsdrv_makevartable(void)
{
	char temp[256];

	addvar( VAR_VALUE, "serialnumber", "Specify serial number, because it cannot detected automagically (default="DEFAULT_SERIALNUMBER")" );

	snprintf( temp, 256, "Specify battery voltage when UPS change state from OB to LB (min=%2.1fV, max=%2.1fV, default=%2.1f)", 
		(double)BATT_DISCHARGED_VOLT/10.0, (double)BATT_MAX_OB_VOLTAGE/10.0, (double)BATT_MIN_OB_VOLTAGE/10.0 );
	addvar( VAR_VALUE, "minbattvolt", temp );

	addvar( VAR_VALUE, "debug", "Specify this param if you want to debug driver" );
}
