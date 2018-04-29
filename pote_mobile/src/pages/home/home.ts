import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { PotesProvider } from '../../providers/potes/potes';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
  potesList:any;

  constructor(public navCtrl: NavController, 
    private potesProvider:PotesProvider) {
      this.getPotes();
    }

    getPotes(){
      this.potesProvider.getPotes().subscribe((potes) => {
      this.potesList = potes;
    
  })

  console.log('Potes',this.potesList)
  }
}
