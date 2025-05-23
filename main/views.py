from flask import render_template, request, redirect, url_for, flash, abort
from . import main
from ..request import get_movies, get_movie, search_movie
from .forms import ReviewForm, UpdateProfile, AddToWatchlistForm
from ..models import Review, User, Movie, Watchlist 
from flask_login import login_required, current_user
from .. import db, photos
import markdown2

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    popular_movies = get_movies("popular")
    upcoming_movie = get_movies("upcoming")
    now_showing_movie = get_movies("now_playing")
    title = 'Home - Welcome to The best Movie Review Website Online'

    search_movie = request.args.get('movie_query')
    if search_movie:
        return redirect(url_for('.search', movie_name=search_movie))
    else:
        return render_template('index.html',
                               title=title, 
                               popular=popular_movies,
                               upcoming=upcoming_movie,
                               now_showing=now_showing_movie)

@main.route("/movie/<int:id>")
def movie(id):
    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.query.filter_by(movie_id=id).all()
    add_to_watchlist_form = AddToWatchlistForm()
    return render_template('movie.html',
                           id=id, 
                           title=title,
                           movie=movie,
                           reviews=reviews,
                           add_to_watchlist_form=add_to_watchlist_form)

@main.route('/search/<movie_name>')
def search(movie_name):
    '''
    View function to display the search results
    '''
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'search results for {movie_name}'
    return render_template('search.html',
                           title=title, 
                           movies=searched_movies)

@main.route('/movie/review/new/<int:id>', methods=['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        rating = form.rating.data
        new_review = Review(movie_id=movie.id,
                            movie_title=movie.title,
                            image_path=movie.poster,
                            review_title=title,
                            movie_review=review,
                            rating=rating,
                            user=current_user)
        new_review.save_review()
        return redirect(url_for('main.movie', id=movie.id))

    title = f'{movie.title} review'
    return render_template('new_review.html',
                           title=title, 
                           review_form=form, 
                           movie=movie)

@main.route("/review/<int:id>")
def single_review(id):
    review = Review.query.get(id)

    if review is None:
        abort(404)
    format_review_title = markdown2.markdown(review.review_title,
                                             extras=["code-friendly", "fenced-code-blocks"])
    format_review = markdown2.markdown(review.movie_review,
                                       extras=["code-friendly", "fenced-code-blocks"])

    return render_template("review.html", 
                           review=review,
                           format_review_title=format_review_title,
                           format_review=format_review)

@main.route("/user/<uname>")
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    title = user.username

    return render_template("profile/profile.html",
                           user=user,
                           title=title)

@main.route("/user/<uname>/update", methods=["GET", "POST"])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.profile", uname=user.username))

    return render_template("profile/update.html", form=form)

@main.route("/user/<uname>/update/pic", methods=["POST"])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if "photo" in request.files:
        filename = photos.save(request.files["photo"])
        path = f"photos/{filename}"
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for("main.profile", uname=uname))

@main.route('/add_to_watchlist/<int:movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    watchlist_item = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if watchlist_item is None:
        watchlist_item = Watchlist(user_id=current_user.id, movie_id=movie.id)
        db.session.add(watchlist_item)
        db.session.commit()
        flash('Movie added to your watchlist!', 'success')
    return redirect(url_for('main.watchlist'))

@main.route('/remove_from_watchlist/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_watchlist(movie_id):
    watchlist_item = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if watchlist_item:
        db.session.delete(watchlist_item)
        db.session.commit()
        flash('Movie removed from your watchlist!', 'success')
    return redirect(url_for('main.watchlist'))

@main.route('/watchlist')
@login_required
def watchlist():
    watchlist_items = Watchlist.query.filter_by(user_id=current_user.id).all()
    return render_template('watchlist.html', watchlist_items=watchlist_items)
