{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1, 2, 3, 4, 5, 6, 6, 7, 8, 9]\n"
     ]
    }
   ],
   "source": [
    "data = [9, 5, 7, 6, 6, 4, 3, 8, 1, 2]\n",
    "\n",
    "def insert_sort(data):\n",
    "    for i in range(1,len(data)):\n",
    "        insert = data[i]\n",
    "        j = i - 1\n",
    "        while j>=0 and data[j]>insert:\n",
    "            data[j + 1] = data[j]\n",
    "            j = j - 1\n",
    "        data[j + 1] = insert\n",
    "        \n",
    "insert_sort(data)\n",
    "print(data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
