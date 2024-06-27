import React from 'react';
import StarRatings from 'react-star-ratings';

function PolarityRating({ polarity }) {
    // Convertir la polaridad (0.0 - 1.0) a una calificación de 5 estrellas
    const rating = polarity * 5;

    return (
        <div>
            <StarRatings
                rating={rating}
                starRatedColor="gold"
                numberOfStars={5}
                starDimension="25px"
                starSpacing="2px"
                name='rating'
            />
        </div>
    );
}

export default PolarityRating;