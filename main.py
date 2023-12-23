import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")
sns.set_palette('viridis')

from prediction import Predictor

# Определите функцию для проверки данных
def check_data(SNILS, BirthDate, Position, JobStartDate, Value, MonthProfit,
               MonthExpense, Merch_code, Loan_amount, Loan_term, Family_status):
    errors = []

    if not SNILS:
        errors.append("Введите корректное значение СНИЛС.")

    if not BirthDate:
        errors.append("Укажите дату рождения.")

    if not Position:
        errors.append("Укажите должность.")

    if not JobStartDate:
        errors.append("Укажите дату начала работы.")

    if not Value:
        errors.append("Укажите стаж работы.")

    if not MonthProfit:
        errors.append("Укажите заработок.")

    if not MonthExpense:
        errors.append("Укажите траты.")

    if not Family_status:
        errors.append("Укажите семейное положение.")

    if not Merch_code:
        errors.append("Укажите код магазина.")

    if not Loan_amount:
        errors.append("Укажите сумму кредита.")

    if not Loan_term:
        errors.append("Укажите срок кредита.")

    return errors


def main():
    st.title('Возможность получения кредита')

    Gender = st.radio(
        "Укажите пол",
        ["Муж.", "Жен."], horizontal=True)

    col1, col2 = st.columns(2)

    with col1:
        contSnils = st.container()
        container1 = st.container()

        SNILS = contSnils.text_input('СНИЛС', value=None)
        if SNILS and (SNILS not in ('0', '1')):
            contSnils.error("Некорректное значение СНИЛС. Введите 0, либо 1.")
        SNILS = int(SNILS)
        BirthDate = container1.date_input("Дата рождения", value=None, format='DD/MM/YYYY')

        Family_status = container1.selectbox('Семейное положение',
                                             ('Никогда в браке не состоял(а)', 'Женат / замужем',
                                              'Разведён / Разведена', 'Гражданский брак / совместное проживание',
                                              'Вдовец / вдова'), index=None, placeholder="Укажите семейный статус")

    with col2:
        container2 = st.container()

        Position = container2.text_input('Должность')

        JobStartDate = container2.date_input("Дата начала работы", value=None, format='DD/MM/YYYY')

        Value = container2.selectbox('Стаж',
                                     ('менее 4 месяцев', '4 - 6 месяцев', '6 месяцев - 1 год',
                                      '1 - 2 года', '2 - 3 года', '3 - 4 года', '4 - 5 лет',
                                      '5 - 6 лет', '6 - 7 лет', '7 - 8 лет', '8 - 9 лет',
                                      '9 - 10 лет', '10 и более лет'), index=None, placeholder="Укажите стаж")
        MonthProfit = container2.number_input('Заработок')
        MonthExpense = container2.number_input('Траты')

        contMerch_code = st.container()
        Merch_code = contMerch_code.text_input('Код магазина')
        if Merch_code:
            try:
                child_count_value = int(Merch_code)
                if child_count_value < 0:
                    contMerch_code.error("Код магазина не может быть отрицательным.")

            except ValueError:
                contMerch_code.error("Некорректное значение. Введите число.")
        Merch_code = int(Merch_code)

    container3 = st.container(border=True)
    Loan_amount = container3.number_input('Сумма кредита')
    Loan_term = container3.select_slider('Срок кредита', options=[6, 12, 18, 24])

    if st.button("Отправить"):

        # Проведите проверку данных
        errors = check_data(SNILS, BirthDate, Position, JobStartDate, Value, MonthProfit,
                            MonthExpense, Merch_code, Loan_amount, Loan_term, Family_status)

        # Если есть ошибки, выделите красным соответствующие элементы
        if errors:
            st.error("Пожалуйста, исправьте следующие ошибки:")
            for error in errors:
                st.error(error)
        else:
            predictor = Predictor()
            predictions = predictor.predict_decision([Position, Gender, MonthProfit, MonthExpense, SNILS, BirthDate,
                                                      JobStartDate, Value, Family_status, Loan_term, Loan_amount,
                                                      Merch_code])

            fig, ax = plt.subplots()

            columns = ['BankA', 'BankB', 'BankC', 'BankD', 'BankE']

            ax.bar(columns, predictions)
            st.pyplot(fig)

if __name__ == '__main__':
    main()