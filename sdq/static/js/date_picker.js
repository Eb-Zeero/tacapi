const start_date = document.querySelector('#start-date');
const end_date = document.querySelector('#end-date');
const submit = document.querySelector('#submit-dates');
const refresh = document.querySelector('#refresh-dates');

function dateChange(event) {
    const name = event.target.name;
    const value = event.target.value;

    document.cookie = `${name}=${value}; expire=; path=/dq`
}


function resetDate(event) {
    let today = new Date();
    const end_date = moment(today).format('YYYY-MM-DD');
    const start_date = moment(today).subtract(90, 'day').format('YYYY-MM-DD');

    console.log(end_date, start_date)
    document.cookie = `start-date=${startDate}; expire=; path=/dq`
    document.cookie = `end-date=${endDate}; expire=; path=/dq`
}

start_date.addEventListener('change', dateChange);
end_date.addEventListener('change', dateChange);
refresh.addEventListener('click', resetDate);
