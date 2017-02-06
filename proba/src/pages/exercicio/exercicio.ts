import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { RESTFULService } from '../../app/services/restful.service';
import { DetailsPage } from '../details/details';

@Component({
  selector: 'exercicio',
  templateUrl: 'exercicio.html'
})
export class ExercicioPage {
  items:  any;
  result: any;
  category: any;
  limit:any;
  constructor(public navCtrl: NavController, private restService:RESTFULService) {
    this.getDefaults();
  }

  ngOnInit(){
    this.getPosts('exercicio');
  }

  getDefaults(){
    if(localStorage.getItem('category') != null){
      this.category = localStorage.getItem('category');
    } else {
      this.category = 'sports';
    }

    if(localStorage.getItem('limit') != null){
      this.limit = localStorage.getItem('limit');
    } else {
      this.limit = 10;
    }
  }

  getPosts(target){
    this.restService.get(target).subscribe(response => {
      this.items = response.result;
      console.log(this.items);
      this.result = response.result.exercicio;
    });
  }

  viewItem(item){
    this.navCtrl.push(DetailsPage, {
      item:this.items
    });
  }

  // changeCategory(){
  //   this.getPosts(this.category, this.limit);
  // }

}
