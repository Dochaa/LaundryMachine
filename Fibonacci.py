from flask import Flask, request, jsonify

app = Flask(__name__)

def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_num = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_num)
    return fib_sequence

@app.route('/calculate_fibonacci/<int:member_count>', methods=['GET'])
def calculate_fibonacci(member_count):
    if member_count < 1 or member_count > 100:
        return jsonify({'error': 'Member count should be between 1 and 100.'}), 400
    
    fib_sequence = fibonacci(member_count)
    total = sum(fib_sequence)
    
    response = {
        'member-count\n': member_count,
        'sequence\n': fib_sequence,
        'total\n': total
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
