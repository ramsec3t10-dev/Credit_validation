**Loan Details**

loan_amnt – Loan amount requested by the borrower

term – Loan repayment duration (in months)

int_rate – Interest rate of the loan

installment – Monthly EMI amount

purpose – Purpose of the loan

grade – Credit grade assigned by the lender (A–G)

sub_grade_num – Encoded sub-grade representing finer credit risk

initial_list_status – Loan listing type

**Applicant Information**

emp_length – Employment length in years

home_ownership – Housing status of the borrower

annual_inc – Annual income of the borrower

annual_inc_missing – Indicator for missing income information

verification_status – Income verification status

application_type – Individual or joint application

**Credit History**

dti – Debt-to-income ratio

delinq_2yrs – Number of delinquencies in the last 2 years

inq_last_6mths – Credit inquiries in the last 6 months

open_acc – Number of currently open credit accounts

total_acc – Total number of credit accounts ever held

revol_bal – Outstanding revolving credit balance

revol_util – Revolving credit utilization percentage

acc_now_delinq – Number of currently delinquent accounts

collections_12_mths_ex_med – Non-medical collections in last 12 months

pub_rec – Number of public derogatory records

pub_rec_bankruptcies – Number of bankruptcies

tax_liens – Number of tax liens

**Time-Based Features (Engineered)
**
issue_year – Year the loan was issued

issue_month – Month the loan was issued

credit_history_years – Length of credit history in years