import { Component, EventEmitter, Input, OnInit, Output, SimpleChanges } from '@angular/core';
import { Client } from 'src/app/constants/model';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {

  @Input() clients: Client[] = [];
  @Output() clientSelected = new EventEmitter<Client>();
  selectedClient!: Client;
  web_page_type: string = 'irah/chat/financial_planner';
  client_name: string = '';

  ngOnInit(){
    if (this.clients.length > 0) {
      this.selectedClient = this.clients[0];
      this.client_name = this.selectedClient.client_data.name;
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['clients'] && changes['clients'].currentValue.length > 0 && !this.selectedClient) {
      this.selectedClient = this.clients[0];
      this.client_name = this.selectedClient.client_data.name;
    }
  }
  
  onSelectClient(client: Client) {
    this.selectedClient = client;
    this.clientSelected.emit(client); 
  }  
}
