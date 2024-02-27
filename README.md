<h1 align="center">lamblbs</h1>
<h2 align="center">Unofficial Lambdalabs CLI</h2>
<p align="center"><strong>⚡ Minimalistic CLI to manage your Lambdalabs Cloud instances ⚡</strong></p>

------------------------------------------------------------------------

## Introduction

This is a personal project that helped me automate the provisioning and deprovisioning of Lambdalabs Cloud instances while I was playing with [Ray on-prem clusters](https://docs.ray.io/en/latest/cluster/vms/user-guides/launching-clusters/on-premises.html). I thought it might be useful for others and decided to share it for anyone to use it. This CLI is leveraging the Lambdalabs [API](https://cloud.lambdalabs.com/api/v1/docs), but it is by no means endorsed by or associated with the Lambdalabs company.

## Pre-requisites

Configure your Lambdalabs API key using

```
export LAMBDALABS_API_KEY=....
```

## Installation

```
pip install lamblbs
```

## Usage

### List instance types 

```bash
lamblbs instance types
```

### List running instances

```bash
lamblbs instance show-all
```

### Launch a new instance

```bash
lamblbs instance launch \
--name ray-head-node \
--type gpu_1x_a10 \
--region us-west-1 \
--ssh_key lambdalabs-ssh-ray \
--qty 1
```

NOTE: This assumes you've created the `lambdalabs-ssh-ray` before hand.

### Check and wait for your instances to be active

```bash
lamblbs instance check-status --status active
```

There are other supported commands as well which can be displayed using:

```bash
lamblbs --help
```
