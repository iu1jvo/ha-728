#!/usr/bin/with-contenv bashio
# Read options from the HA add-on configuration and pass them
# to the Python daemon as environment variables.

bashio::log.info "Starting X728 UPS Daemon..."

export HW_VERSION=$(bashio::config 'hw_version')
export DAEMON_PORT=$(bashio::config 'daemon_port')
export POLL_INTERVAL=$(bashio::config 'poll_interval')
export SHUTDOWN_VOLTAGE=$(bashio::config 'shutdown_voltage')
export SHUTDOWN_CAPACITY=$(bashio::config 'shutdown_capacity')
export SHUTDOWN_DELAY=$(bashio::config 'shutdown_delay')
export BUZZER_ON_AC_LOSS=$(bashio::config 'buzzer_on_ac_loss')

bashio::log.info "hw_version:        ${HW_VERSION}"
bashio::log.info "daemon_port:       ${DAEMON_PORT}"
bashio::log.info "poll_interval:     ${POLL_INTERVAL}s"
bashio::log.info "shutdown_voltage:  ${SHUTDOWN_VOLTAGE}V"
bashio::log.info "shutdown_capacity: ${SHUTDOWN_CAPACITY}%"
bashio::log.info "shutdown_delay:    ${SHUTDOWN_DELAY}s"
bashio::log.info "buzzer_on_ac_loss: ${BUZZER_ON_AC_LOSS}"

exec python3 /app/x728_daemon.py
