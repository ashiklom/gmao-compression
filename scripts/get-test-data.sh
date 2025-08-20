#!/usr/bin/env bash

mkdir -p _data

wget -nc -P _data \
  https://portal.nccs.nasa.gov/datashare/gmao/geos-s2s-3/GiOCEAN_e1/subdaily/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_0600z.nc4 \
  https://portal.nccs.nasa.gov/datashare/gmao/geos-s2s-3/GiOCEAN_e1/subdaily/GiOCEAN_e1.atm_inst_6hr_glo_L720x361_p49.20241101_1800z.nc4 \
  https://portal.nccs.nasa.gov/datashare/gmao/geos-s2s-3/GiOCEAN_e1/subdaily/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_0730z.nc4 \
  https://portal.nccs.nasa.gov/datashare/gmao/geos-s2s-3/GiOCEAN_e1/subdaily/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.20241101_1930z.nc4
