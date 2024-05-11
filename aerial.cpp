#include <bits/stdc++.h>
#include <random>
#include <iostream>
using namespace std;
// getting date to string 
string getCurrentDateAsString() {
    time_t currentTime = time(nullptr);
    tm* localTime = localtime(&currentTime);
    char buffer[80];
    strftime(buffer, 80, "%Y-%m-%d", localTime);
    string currentDate(buffer);
    return currentDate;
}

string Date;
// Function to check uniqueness of username 

vector<string>user ;
 int  uniqueusername( string s ){
      bool flag = 0 ;
        for ( int i = 0 ; i < user.size() ; i++){
            if ( user[i].size() == s.size()){
            for ( int j = 0 ; j < user[i].size() ; j++){
                     if ( s[j] == user[i][j]){
                        flag = true ;
                     }  
                     else {
                        flag = false ;
                        break;
                     }
            }
                if ( flag ){
                    return 1 ; 
                }
            }
        }
        user.push_back(s);
    return 0 ;
 }

long number = 567843292;
class BankAccountHolder{
       string  password;
     public :
      string Name;
      string Username;
      vector<pair<long,string> >list_of_accounts;
      void getaccounts();
      void change_password();
      void create_accounts();
      void New_user ();
};
vector< BankAccountHolder* > BankAccountHolderINSTANCES;

class BankAccount : public BankAccountHolder{
    public :
    long accountno ;
    int Balance ;
    char Accounttype;
    string opendate;
    vector < pair<string , int> > statements;
    void deposit(long a , int b);
    void withdraw(long a , int b);
    void transfer (long a , int b);
    vector<pair<string ,int > > *  getstatements();
};


class BankManager {
    public:
    string username ;
    string password ;
    void getAccountHolder ();
    void getStatementsofAccount(long a);
    void fast_forward(long a , int b );
};
// account holder login 
void BankAccountHolder::New_user(){
       std::cout << " Enter your name " <<endl;
       std::cin >> Name;
       std::cout << " Enter your username " <<endl;
       std::cin >> Username ;
       while ( true){
       if (uniqueusername(Username )){
              std::cout<<"This Username already exist "<<endl ;
              std::cout <<"Please another Username " <<endl;
              std::cin >> Username ;
        
       }
       else {
              break;
       }
       }
       std::cout << " Make a strong password " <<endl;
       std::cin >> password;
       string temp;
       bool flag = false;
       while(!flag){
       std::cout << " Confirm password " <<endl;
       std::cin >> temp ;
       for ( int i = 0; i < password.size() ; i++){
           if (temp[i] == password[i]){
            flag = true;
           }
           else {
            flag = false;
            break;
           }
       }
       if(flag){
        std::cout << " Congrats !! You have logged in Successfully "<<endl;
       }
       else {
        std::cout << " Password did not match " <<endl;
       }
       }
}


// change_password
void BankAccountHolder :: change_password(){
          std::cout<<" Enter your Existing password " <<endl;
          string temp;
          std::cin >>temp;
          bool flag = false ;
          for ( int i = 0 ; i < password.size() ; i++){
            if ( password[i] == temp[i]){
                flag = true;

            }
            else {
                std::cout<<"Password did not match try after sometime " <<endl;
                flag = false;
                break;
            }
          }
          if ( flag ){
            std::cout << "Enter your new password " <<endl;
            std::cin >> temp ;
            std::cout << "Confirm password " <<endl;
            string t1;
            std::cin >> t1;
            flag  = false ;
             while(!flag){
       std::cout << " Confirm password " <<endl;
       std::cin >> temp ;
       for ( int i = 0; i < password.size() ; i++){
           if (temp[i] == password[i]){
            flag = true;
           }
           else {
            flag = false;
            break;
           }
       }
       if(flag){
          password.clear();
           for ( int i = 0 ; i < temp.size() ; i++){
                password.push_back(temp[i]);
           }
           std::cout << " Password have been successfully changed " <<endl;
       }
       else {
        std::cout << " Password did not match " <<endl;
       }
       }
          }
}  
    vector< BankAccountHolder* >Pa ;
    vector <BankAccount*> ca;


void BankAccountHolder :: getaccounts(){
                            for (int i =0 ; i< list_of_accounts.size() ; i++ ) {
                                  std::cout << "(" << list_of_accounts[i].first << ", " << list_of_accounts[i].second << ")" << endl;
                             }
}

void BankAccount :: deposit(long a , int b){
   
             for ( int i = 0 ; i < ca.size() ; i++ ){
                   if ( ca[i]->accountno == a){
                      ca[i]->Balance += b;
                      ca[i]->statements.push_back(make_pair("Money Deposited " ,b ));
                   }
             }
}

void BankAccount :: withdraw(long a , int b ){
    
           for ( int i = 0 ; i < ca.size() ; i++ ){
                   if ( ca[i]->accountno == a){
                      ca[i]->Balance -= b;
                      ca[i]->statements.push_back(make_pair("Money Withdrawn " ,b ));
                   }
             }
}

void BankAccount :: transfer(long a , int b){
   
      for ( int i = 0 ; i < ca.size() ; i++ ){
                   if ( ca[i]->accountno == a){
                      ca[i]->Balance -= b;
                      ca[i]->statements.push_back(make_pair("Money Transfered " ,b ));
                   }
             }
}

void BankManager :: getStatementsofAccount(long a){
           for  ( int i  = 0 ; i< ca.size() ; i++){
                   long  temp = ca[i]->accountno;
                  
                   if ( temp == a){
                       for ( int j = 0  ; j< ca[i]->statements.size( ) ; j++) {
                                  std::cout << "(" <<  ca[i]->statements[j].first << ", " << ca[i]->statements[j].second << ")" << endl;
                             }
                            break;
                           }
                   }
                   
 }
           
void BankManager :: getAccountHolder(){
      for ( int i = 0 ; i < Pa.size() ; i++){
           std::cout <<  Pa[i]->Name <<endl;
           for (int j = 0  ;j < Pa[i]->list_of_accounts.size() ; j++) {
                                  std::cout << "(" << Pa[i]->list_of_accounts[j].first << ", " << Pa[i]->list_of_accounts[j].second << ")" << endl;
            }
      }
}
class saving_account : public BankAccount{
     public:
     float interest_rate;
      float getinterestrate();
     void  setinterestrate(int a);
};

vector<saving_account*>sa;
class Checking_account : public BankAccount{
    public:
    float interest_rate ;
    void get_interest();
};
vector<Checking_account*>cra;

void saving_account :: setinterestrate(int a){
            float lastdigit ;
            int count =0 ;
            int temp = a;
            while(a>0){
                  lastdigit = a%10;
                  a = a/10; 
                  count ++; 
            }

            interest_rate = ((temp/pow(10,count+1)) * lastdigit)/6;
}


void Checking_account :: get_interest(){
    std::cout<<"Interest rate is zero . Hence increment in your balance is zero "<<endl;
}

void BankManager :: fast_forward( long a , int b){
    int i ;
             for  (  i = 0 ; i < sa.size( ) ; i++ ){
                  if ( sa[i] -> accountno == a){
                    for ( int j = 0 ;  j < b ; j++ ){
                          sa[i] -> Balance = sa[i]->Balance * ( 1 + sa[i]->interest_rate/365);
                    }
                  }
             }
             for ( int  j= 0 ; j < ca.size() ; j++){
                if (ca[j]->accountno == a){
                    ca[j]->Balance = sa[i]->Balance;
                }
             }
}
float saving_account :: getinterestrate(){
    // float returnvalue;
    //     for ( int i = 0 ; i < ca.size() ; i++ ){
    //          if ( ca[i]->accountno == a){
    //             returnvalue = ca[i]->Balance;
    //             for ( int j = 0 ; j < d ; j ++ ){
    //                     returnvalue = returnvalue *(1+(interest_rate/365));
    //             }
    //          }
    //          ca[i]->Balance += returnvalue ;
    //     }
    //     return returnvalue;
    return interest_rate;

}
 vector<pair<string ,int > > *  BankAccount ::  getstatements(){
         return &statements ;
 }

 BankAccount* search(long a){
    for ( int i = 0 ; i < ca. size() ; i ++){
        if ( ca[i]->accountno == a){
             return ca[i];
        }
    }
    return ca[0];
 }
 
 BankAccountHolder * accountlogin(){
       string u;
       std::cout << "Enter your Username " <<endl;
       std::cin >> u;
       std::cout << "Enter your password " <<endl;
       string p;
       std::cin>>p;
       for ( int i  = 0 ; i < Pa.size() ; i++ ){
           string temp = Pa[i]->Username;
            bool flag = false;
           if ( temp.size() == u.size()){
            for  ( int j = 0 ; j <  u.size() ; j++){
                if ( temp[j] == u[j]){
                    flag =true;
                }
                else{
                    flag = false;
                    break;
                }
            }
           }
           if ( flag){
               std::cout<< Pa[i]->Name<<endl;
                return Pa[i];
           }
       }
       return NULL;
 }

BankManager*bm;
BankManager*  blogin (){
    std::cout<<"Enter the username "<<endl;
    string s;
    cin>>s;
    std::cout<<"Enter the password "<<endl;
    string p;
    cin>>p;
        bool flag = false ;
    for ( int i = 0 ; i < bm->password.size() ; i++){
        if ( bm->password[i] == p[i]){
            flag = true ;
        }
        else {
            flag = false;
            cout <<"Wrong Password , Try After sometime "<<endl;
        }
    }
    if ( flag ){
        return bm;
    }
    return NULL;
}


void BankAccountHolder :: create_accounts(){
        BankAccount *B1 = new BankAccount() ;
        ca.push_back(B1);
        B1->accountno = number ;
        B1->opendate = getCurrentDateAsString();
        std::cout<<"what type of account do you want to get " <<endl;
        std::cout<<"1.Saving account or 2.Checking account "<<endl;
        std::cout <<"1 or 2"<<endl;
        int x;
        cin>>x;
        std::cout<<"Enter a opening balance of at least 2000 rupees " <<endl;
        int n;
        std::cin >>n;
        B1->Balance = n;
        if (x == 1){
            B1->Accounttype = 's';
            saving_account *sac = new saving_account(); 
            sa.push_back(sac);
            sac->accountno = number;
            sac->Balance = n;
            list_of_accounts.push_back(make_pair(B1->accountno , "Saving account"));
        }
        else{
             B1->Accounttype = 'c';
             Checking_account* cac = new Checking_account();
             cra.push_back(cac);
             cac->accountno = number;
             cac->Balance = n;
            list_of_accounts.push_back(make_pair(B1->accountno,"Checking account"));
        }
        std::cout << "Congrats!! Your has been created successfully with account no "<<number <<endl;
        number ++;
}  

saving_account* search1(long a ){
    for ( int i = 0 ; i <sa.size() ; i++){
        if ( sa[i]->accountno == a){
            return sa[i];
        }
    }
    return NULL;
}
Checking_account* search2(long a){
     for ( int i = 0 ; i <cra.size() ; i++){
        if ( cra[i]->accountno == a){
            return cra[i];
        }
    }
    return NULL;
}
int main(){
      Date = getCurrentDateAsString() ;
      int n ;
      int x;
      bm = new BankManager();
      bm->username = "Aerial";
      bm->password = "Robotics";
      while(true){
        std::cout<< "                  0. Are you a new user ? " <<endl; 
        std::cout<< "                  1. Account Holder Login "<<endl;
        std::cout<< "                  2. Branch Manager Login "<<endl;
        std::cout<< "                  3. Do you want to do some transactions ? " <<endl;
        std::cout<< "                  4. Want to setinterestrate " <<endl;
        std::cout<< "                  5. Want to getinterestrate" <<endl;
        std::cout<< "                  6. Do you want to exit the program  ? " <<endl;
        std::cout<< "                            0 or 1 or 2 or 3 or 4 or 5 or 6   "<<endl;

        std::cin >>n; 

      if ( n == 6 ){
        break;
      }
      if ( n==0){
           BankAccountHolder* obj = new BankAccountHolder();
           obj->New_user();
           Pa.push_back(obj);
      }
      else if ( n == 1){
          BankAccountHolder* obj = accountlogin();
          std::cout<<" Choose from the following " <<endl;
          std:: cout << " 1.Do you want to creat new account  " <<endl;
          std:: cout <<"  2.Do you want to see all your accounts "<<endl;
          std:: cout << " 3.Do you wnat to change your password "<<endl;
          int c;
          std::cin>>c;
          if(c==1){
          obj ->create_accounts();
          }
          if ( c==2){
            obj->getaccounts();
          }
          if ( c==3){
            obj->change_password();
          }
      }
      else if ( n==3){
        long a ;
       std:: cout << " Enter your Bank account no " <<endl;
        std::cin >>a ;
          BankAccount* obj = search (a);
          std::cout<<"Choose the type of transaction from below ";
          std::cout<<" 1.Want to Deposit the money  ";
          std::cout<<" 2. Want to transfer the money ";
          std::cout<<" 3. Want to withdraw the  money ";
          std::cout<<" 4.Want to know your current Balance ";
          std::cout<<" 5.Want to see your all transactions ";
          int x ;
           std::cin >>x;
           if ( x == 1){
            int b;
             std::cout<<" Transaction of rupees above 50000 is not allowed " <<endl;
            std::cout<<"Enter the amount of money " <<endl;
            std::cin >> b;
             obj->deposit(a , b);
           }
           if ( x==2){
                int b;
                 std::cout<<" Transaction of rupees above 50000 is not allowed " <<endl;
            std::cout<<"Enter the amount of money " <<endl;
            std::cin >> b;
             obj->transfer(a , b);
           }
           if ( x==3){
                 int b;
                  std::cout<<" Transaction of rupees above 50000 is not allowed " <<endl;
            std::cout<<"Enter the amount of money " <<endl;
            std::cin >> b;
             obj->withdraw(a , b);
           }
           if ( x==4){
            std::cout<<"Your current Balance is " << obj->Balance <<endl;
           }
           if ( x== 5 ){
             for ( int i = 0;i < obj->statements.size() ; i++){
                cout <<"( "<< obj->statements[i].first <<" , " << obj->statements[i].second<<" )"<<endl;
             }
           }
      }
      else if ( n == 2){
          BankManager* b = blogin();
          if (b!=NULL){

          
          std::cout << "Choose from the following choices "<<endl;
          std::cout << "1.Want list of all account holders   "<<endl;
          std::cout << "2.Want the statements of a particular account"<<endl;
          std::cout << "3.Want to apply fast forward to a particular account"<<endl;

          int x ; 
          cin >>x;
          if ( x==1){
              bm->getAccountHolder();
          }
          if (x==2){
               std::cout << "Enter the account number " <<endl;
               long a ;
               std::cin >>a;
               bm->getStatementsofAccount(a);
          }
          if ( x==3){
                  std::cout << "Enter the account number " <<endl;
               long a ;
               std::cin >>a;
               std::cout<< "Enter the no of days " <<endl;
               int d ; 
               std::cin >>d;
               bm->fast_forward( a , d );
          }
          }
      }
      else if ( n == 4){
              std::cout << " What is your account type , 1.saving or 2. checking " <<endl;
            int x;
            cin>>x;
            if ( x == 1){
            std::cout << " Enter your account no " << endl;
            long a;
            std::cin>>a;

           saving_account* ss = search1(a);
           ss->setinterestrate(ss->Balance);
            }
            else {
                std::cout<<"Interest rate is Bydefault zero " <<endl;
            }
      }
      else if ( n ==5 ){
            std::cout << " What is your account type , 1.saving or 2. checking " <<endl;
            int x;
            cin>>x;
            if ( x == 1){
            std::cout << " Enter your account no " << endl;
            long a;
            std::cin>>a;
             saving_account* ss = search1(a);
             cout<<"The interest rate is " << ss->getinterestrate() <<endl;
            }
            else {
                std::cout << " Enter your account no " << endl;
                long a;
                Checking_account * cc = search2(x);
                cc->get_interest();
            }
            
      } 
      }
    return 0;
}
