import { Component, Input, OnChanges } from '@angular/core';
import { Client } from 'src/app/constants/model';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements OnChanges {
  @Input() client!: Client;
  retirementData: any[] = []; 
  trustFundData: any[] = [];   
  otherInvestmentsData: any[] = [];  

  backgroundColor = '#0e1117'; 
  textColor = '#ffffff'; 

  ngOnChanges() {
    const yearsToRetirement = this.client.client_data.retirement_age - this.client.client_data.age;

    // Prepare Retirement Accounts Growth Data
    this.retirementData = this.client.client_data.retirement_accounts.map(account => ({
      x: Array.from({ length: yearsToRetirement + 1 }, (_, i) => i),
      y: this.calculateGrowth(account.balance, account.contribution, account.annual_growth, yearsToRetirement),
      mode: 'lines',
      name: account.type
    }));

    // Prepare Trust Fund Accounts Growth Data (similar to retirement)
    this.trustFundData = this.client.client_data.trust_fund_accounts.map(account => ({
      x: Array.from({ length: yearsToRetirement + 1 }, (_, i) => i),
      y: this.calculateGrowth(account.balance, account.contribution, account.annual_growth, yearsToRetirement),
      mode: 'lines',
      name: `Trust Fund for ${account.beneficiary}`
    }));

    // Prepare Other Investments Growth Data (similar to retirement)
    this.otherInvestmentsData = this.client.client_data.other_investments.map(investment => ({
      x: Array.from({ length: yearsToRetirement + 1 }, (_, i) => i),
      y: this.calculateGrowth(investment.balance, 0, investment.annual_growth, yearsToRetirement),
      mode: 'lines',
      name: investment.type
    }));
  }

  calculateGrowth(balance: number, contribution: number, annual_growth: number, years: number): number[] {
    let amounts = [];
    for (let year = 0; year <= years; year++) {
      amounts.push(balance);
      balance += contribution + balance * annual_growth;
    }
    return amounts;
  }

}

