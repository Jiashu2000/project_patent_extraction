from utils import generate_random_start, generate_from_seed
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request
from wtforms import Form, StringField, validators, SubmitField, DecimalField, IntegerField

app = Flask(__name__)

class ReusableForm(Form):
    """user entry form for entering specifics for generation"""

    # starting seed
    seed = StringField("Enter a seed string or 'random: ", validators = [validators.InputRequired()])

    # diversity of predictions
    diversity = DecimalField("Enter diversity: ", default = 0.8,
                             validators = [validators.InputRequired(),
                                           validators.NumberRange(min = 0.5, max = 5.0,
                                                                  message='Diversity must be between 0.5 and 5.')])
    
    # number of words
    words = IntegerField("Enter number of words to generate:",
                         default=50, validators= [validators.InputRequired(),
                                                  validators.NumberRange(min = 10, max = 100, 
                                                                         message = 'Number of words must between 10 and 100')])
    
    # submit button
    submit = SubmitField("Enter")

def load_keras_model():
    """load in the pre-trained model"""
    global model
    model = load_model("models/pre-trained-rnn.h5")
    # required for model to work
    global graph
    graph = tf.compat.v1.get_default_graph()


# Home page
@app.route('/', methods = ['GET', 'POST'])
def home():
    """home page of app with form"""
    # create form
    form = ReusableForm(request.form)

    # on form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # extract information
        seed = request.form['seed']
        diversity = float(request.form['diversity'])
        words = int(request.form['words'])
        # generate a random sequence
        if seed == 'random':
            return render_template('random.html', input=generate_random_start(new_words=words, diversity= diversity))
        # generate starting from a seed sequence
        else:
            return render_template('seeded.html', input=generate_from_seed(seed, new_words=words, diversity= diversity))
    
    # send template information to index.html
    return render_template('index.html', form = form)

if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    app.run(host ='0.0.0.0', port = 10)

