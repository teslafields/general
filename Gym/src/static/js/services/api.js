class API{
    constructor(){
        this.rootUrl = 'http://10.5.0.16:8000/',
        this.authentication = btoa("benhurzi@gmail.com:pierin2017")
    }

    prepareUrl(endpoint, querystring=null){
        if (endpoint.startsWith('/')){
          endpoint =endpoint.substring(1);
        }

        if (!endpoint.endsWith('/')){
            endpoint = endpoint + '/';
        }

        return `${this.rootUrl}${endpoint}`
    }

    get(url, auth=true){
        let settings = {
            url: url,
            method: "GET",
            headers: {
                "Authorization": "Basic " + this.authentication
              },
            dataType: "json"
        }

        return $.ajax(settings)
    }

    post(url, data, auth=true){
        let settings = {
            url: url,
            method: "POST",
            headers: {
                "Authorization": "Basic " + this.authentication
              },
            dataType: "json"
        }
        if (data) {
            settings.data = data
        }
        return $.ajax(settings)
    }

    put(url, data, auth=true){
        let settings = {
            url: url,
            method: "PUT",
            headers: {
                "Authorization": "Basic " + this.authentication
              },
            data: data,
            dataType: "json"
        }

        return $.ajax(settings)
    }

    patch(url, data, auth=true){
        let settings = {
            url: url,
            method: "PATCH",
            headers: {
                "Authorization": "Basic " + this.authentication
              },
            data: data,
            dataType: "json"
        }

        return $.ajax(settings)
    }

    delete(url, auth=true){
        let settings = {
            url: url,
            method: "DELETE",
            dataType: "json",
            headers: {
                "Authorization": "Basic " + this.authentication
              },
        }

        return $.ajax(settings)
    }
}
