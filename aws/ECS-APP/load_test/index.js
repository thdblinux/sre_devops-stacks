import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    vus: 5,
    duration: '3000s',
};

const params = {
    headers: {
        'Contnt-Type': 'application/json',
        'Host': 'chip.mandalor.demo'
    },
};

export default function () {
    http.get('http://mandalor-ecs-cluster-ingress-786709273.us-east-1.elb.amazonaws.com/burn/system')
    sleep(1);
}