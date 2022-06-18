import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  changeRating = (id, rating) => {
    let questions = [...this.state.questions]
    let targetQuestion = questions.find((question) => question.id === id);

    $.ajax({
      url: `/questions/${id}`, //TODO: update request URL
      type: "PATCH",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ 'rating': rating }),
      success: (result) => {
        targetQuestion.rating = rating
        this.setState({ questions })
      },
      error: (error) => {
        alert('Unable to update the rating.')
        return;
      }
    })
  }

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {(this.state.categories).map((cat, ind) => (
              <li
                key={cat.id}
                onClick={() => {
                  this.getByCategory(cat.id);
                }}
              >
                {cat.type}
                <img
                  className='category'
                  alt={`${cat.type.toLowerCase()}`}
                  src={`${cat.type.toLowerCase()}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
              rating={q.rating}
              changeRating={this.changeRating}
              {...q}
            />

          ))}
          {this.state.questions.length === 0 && <h5>No Question</h5>}

          {this.state.questions.length === 0 && <div className='pagination-menu'>{this.createPagination()}</div>}
        </div>
      </div>
    );
  }
}

export default QuestionView;
