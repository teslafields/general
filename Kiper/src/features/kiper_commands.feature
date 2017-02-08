# behave --tags ~@delete_ipwall --tags ~@delete_set_rf --tags ~@delete_user --tags ~@delete_guest --tags ~@delete_qrcode_reader --tags ~@update_cpu --tags ~@update_ipwall
Feature: Teste das requisicoes associados ao Protocolo de comunicacao da Kiper entre Server e CPU, versao 1.1

  @ping
  Scenario: requisicao ping
    Given um comando server->cpu "ping"
    Then recebe "sucesso no ack"

  @delete_all_qrcode_readers
  Scenario: requisicao delete_all_qrcode_readers
    Given um comando server->cpu "delete_all_qrcode_readers"
    Then recebe "sucesso no ack"

  @delete_all_guests
  Scenario: requisicao delete_all_guests
    Given um comando server->cpu "delete_all_guests"
    Then recebe "sucesso no ack"

  @delete_all_users
  Scenario: requisicao delete_all_users
    Given um comando server->cpu "delete_all_users"
    Then recebe "sucesso no ack"

  @delete_all_set_rf
  Scenario: requisicao delete_all_set_rf
    Given um comando server->cpu "delete_all_set_rf"
    Then recebe "sucesso no ack"

  @delete_all_ipwalls
  Scenario: requisicao delete_all_ipwalls
    Given um comando server->cpu "delete_all_ipwalls"
    Then recebe "sucesso no ack"

  @insert_ipwall
  Scenario: requisicao insert_ipwall
    given um comando server->cpu "insert_ipwall"
    then recebe "sucesso no ack"

  @insert_set_rf
  Scenario: requisicao insert_set_rf
    Given um comando server->cpu "insert_set_rf"
    Then recebe "sucesso no ack"

  @insert_user
  Scenario: requisicao insert_user
    Given um comando server->cpu "insert_user"
    Then recebe "sucesso no ack"

  @insert_qrcode_reader
  Scenario: requisicao insert_qrcode_reader
    Given um comando server->cpu "insert_qrcode_reader"
    Then recebe "sucesso no ack"

  @insert_guest
  Scenario: requisicao insert_guest
    Given um comando server->cpu "insert_guest"
    Then recebe "sucesso no ack"

  @start_emergency
  Scenario: requisicao start_emergency
    Given um comando server->cpu "start_emergency"
    When recebe o ack do comando
    Then recebe resposta cpu->server "emergency_started"

  @stop_emergency
  Scenario: requisicao stop_emergency
    Given um comando server->cpu "stop_emergency"
    When recebe o ack do comando
    Then recebe resposta cpu->server "emergency_stoped"

  @get_relays_status
  Scenario: requisicao get_relays_status
    Given um comando server->cpu "get_relays_status ipwall_id: 3"
    When recebe o ack do comando
    Then recebe resposta cpu->server "send_relays_status"

  @open_the_door
  Scenario: requisicao open_the_door
    Given um comando server->cpu "open_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"

  @close_the_door
  Scenario: requisicao close_the_door
    Given um comando server->cpu "close_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"

  @keep_the_door_opened
  Scenario: requisicao keep_the_door_opened
    Given um comando server->cpu "keep_the_door_opened ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"

  @close_the_door
  Scenario: requisicao close_the_door
    Given um comando server->cpu "close_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"

  @reset_ipwall
  Scenario: requisicao reset_ipwall
    Given um comando server->cpu "reset_ipwall id: 3"
    When recebe o ack do comando
    Then recebe resposta cpu->server "ipwall_started"

  @update_ipwall
  Scenario: requisicao update_ipwall
    Given um comando server->cpu "update_ipwall"
    When recebe o ack do comando
    Then recebe resposta cpu->server "update_ipwall_result"

  @delete_qrcode_reader
  Scenario: requisicao delete_qrcode_reader
    Given um comando server->cpu "delete_qrcode_reader"
    Then recebe "sucesso no ack"

  @delete_guest
  Scenario: requisicao delete_guest
    Given um comando server->cpu "delete_guest"
    Then recebe "sucesso no ack"

  @delete_user
  Scenario: requisicao delete_user
    Given um comando server->cpu "delete_user"
    Then recebe "sucesso no ack"

  @delete_set_rf
  Scenario: requisicao delete_set_rf
    Given um comando server->cpu "delete_set_rf"
    Then recebe "sucesso no ack"

  @delete_ipwall
  Scenario: requisicao delete_ipwall
    Given um comando server->cpu "delete_ipwall"
    Then recebe "sucesso no ack"

  @vacuum_db
  Scenario: requisicao vacuum_dbs
    Given um comando server->cpu "vacuum_db"
    When recebe o ack do comando
    Then recebe resposta cpu->server "vacuum_done"

# @update_cpu
#  Scenario: requisicao update_cpu
#    Given um comando server->cpu "update_cpu"
#    When recebe o ack do comando
#    Then recebe resposta cpu->server "update_cpu_started"
