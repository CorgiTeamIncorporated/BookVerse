// Sorting features
function get_review_date (obj) {
    let date_str = obj.getElementsByClassName('review-date')[0].innerText;
    let [day, month, year] = date_str.split(".");
    return new Date(year, month - 1, day);
}

function get_review_rating (obj) {
    let rating_node = obj.getElementsByClassName('review-score')[0];

    if (rating_node === undefined) {
        return 0;
    }

    return parseInt(rating_node.innerText);
}

// DOM handling features
let $ = (s) => document.querySelector(s);

function get_reviews_root () {
    return document.getElementById('reviews-outer');
}

function get_all_books () {
    return Array.from(get_reviews_root().children);
}

// Callbacks
function toggleable_book_sort (key) {
    let order = 1;

    return function () {
        let reviews_root = get_reviews_root();
        let sorted_books = get_all_books().sort(
            (a, b) => order * (key(a) - key(b))
        );

        reviews_root.replaceChildren(...sorted_books);

        order *= -1;
    }
}

// Adding listeners
document.addEventListener('DOMContentLoaded', function () {
    $('#date-sort-button').onclick = toggleable_book_sort(get_review_date);
    $('#rating-sort-button').onclick = toggleable_book_sort(get_review_rating);
})
