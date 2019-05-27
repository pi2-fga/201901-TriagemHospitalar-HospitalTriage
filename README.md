# Hospital Triage

Aplicativo para autoatendimento na triagem da emergência hospitalar, escrito usando
django

## Pré requisitos

Para rodar esse projeto os programas docker e docker-compose devem estar previamente instalados.

## Setup

Este projeto permite que um paciente seja orientado no fluxo da triagem hospitalar,
e para isso depende do bot de triagem, disponível em:
https://github.com/pi2-fga/201901-TriagemHospitalar-TriageBot

Além disso, ele persiste os dados coletados da triagem em uma outra aplicação,
que gerencia os pacientes no atendimento de emergência hospitalar:


Para rodar localmente o projeto, os três devem estar na mesma rede, depois que os depois projetos
estejam rodando:

```
$ sudo docker network create triagenetwork
$ sudo docker network connect triagenetwork hospitaltriage_hospital-triage_1
$ sudo docker network connect triagenetwork triagebot_bot_1
$ sudo docker network connect triagenetwork patientmanagement_patient-management_1

```
