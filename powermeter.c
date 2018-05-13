#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <modbus/modbus.h>

int main(int argc, char *argv[]) {

    modbus_t *ctx;
    uint16_t tab_reg[64];
    int rc;
    int i;
    struct timeval old_response_timeout;
    struct timeval response_timeout;

    int reg_start = 0x8900; /* Serial number */
    int reg_howMany = 2; /* 16bits per register */
    const char *devname = "/dev/pm.serial";

    if (argc==3) {
        reg_start = strtol(argv[1], NULL, 0);
        reg_howMany = strtol(argv[2], NULL, 0);
    }

    printf("Opening %s [0x%x] for %d registers\n", devname, reg_start, reg_howMany);
    ctx = modbus_new_rtu(devname, 19200, 'E', 8, 1);
    if (ctx == NULL) {
        fprintf(stderr, "Unable to create the libmodbus context\n");
        return -1;
    }
    modbus_set_slave(ctx, 1);
    modbus_get_response_timeout(ctx, &old_response_timeout);
    printf("response_to = %dsec %dusec", old_response_timeout.tv_sec, old_response_timeout.tv_usec);
    response_timeout.tv_sec = 10;
    response_timeout.tv_usec = 0;
    modbus_set_response_timeout(ctx, &response_timeout);
    modbus_set_byte_timeout(ctx, &response_timeout);
    modbus_set_debug(ctx, TRUE);
    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }

    rc = modbus_read_registers(ctx, reg_start, reg_howMany, tab_reg);
    if (rc == -1) {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return -1;
    }

    for (i=0; i < rc; i++) {
        printf("reg[%d]=%d (0x%X)\n", i, tab_reg[i], tab_reg[i]);
    }

    modbus_close(ctx);
    modbus_free(ctx);
}
