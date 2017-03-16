import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import 'rxjs/Rx';


@Injectable()
export class RESTFULService{
    http:any;
    baseUrl: String;
    user: String;
    passwd: String;

    constructor(http: Http){
        this.http = http;
        this.user = "benhurzi@gmail.com";
        this.passwd = "fitlabcore";
        this.baseUrl = 'http://localhost:5010/'//'http://179.223.188.164:5000/'
    }

    get(target){
        var headers = { headers:{
                                  'Authorization': "Basic "+btoa(this.user+":"+this.passwd)
                                }
                      };
        return this.http.get(this.baseUrl+target, headers).map(res => res.json());
    }

    post(category, limit){
        return this.http.get(this.baseUrl+'/'+category)
            .map(res => res.json());
    }

    update(category, limit){
        return this.http.get(this.baseUrl+'/'+category)
            .map(res => res.json());
    }

    partialup(category, limit){
        return this.http.get(this.baseUrl+'/'+category)
            .map(res => res.json());
    }

    delete(category, limit){
        return this.http.get(this.baseUrl+'/'+category)
            .map(res => res.json());
    }
}
