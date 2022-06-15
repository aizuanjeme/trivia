import React, { Component } from 'react';
import '../stylesheets/Question.css';

// const starArray = [5, 4, 3, 2, 1]

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  // createStars() {
  //   let { id, rating } = this.props;

  //   return (
  //     <div className="rating">
  //       {starArray.map(num => (
  //         <button
  //           type="button"
  //           key={num}
  //           name='rating'
  //           className={`star ${rating >= num ? "active" : "off"}`}
  //           onClick={() => { this.props.changeRating(id, num) }}
  //         >
  //           <span className="star">&#9733;</span>
  //         </button>
  //       ))}
  //     </div>
  //   )
  // }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty, rating, id } = this.props;
    return (
      <>
        <div className='Question-holder'>
          <div className='Question'>{question}</div>
          <div className='Question-status'>
            <img
              className='category'
              alt={`${category.toLowerCase()}`}
              src={`${category.toLowerCase()}.svg`}
            />
            <div className='difficulty'>Difficulty: {difficulty}</div>
            <img
              src='delete.png'
              alt='delete'
              className='delete'
              onClick={() => this.props.questionAction('DELETE')}
            />
          </div>
          {/* {this.createStars()} */}
          <div className="rating">
            {[...Array(5)].map((star, index) => {
              index += 1;
              return (
                <button
                  type="button"
                  key={index}
                  name='rating'
                  className={index <= rating ? "on" : "off"}
                  onClick={() => this.props.changeRating(this.props.id, index)}
                >
                  <span className="star">&#9733;</span>
                </button>
              );
            })}
          </div>
          <div
            className='show-answer button'
            onClick={() => this.flipVisibility()}
          >
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
          <div className='answer-holder'>
            <span
              style={{
                visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
              }}
            >
              Answer: {answer}
            </span>
          </div>

        </div>
      </>
    );
  }
}

export default Question;
