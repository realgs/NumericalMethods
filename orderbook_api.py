{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "sale\n",
      "[6805, 0.0444002]\n",
      "[6893.85, 0.00385758]\n",
      "[6906.99, 0.00918246]\n",
      "[6940, 0.01172679]\n",
      "[6944.95, 0.00368417]\n",
      "[6970.85, 0.00460685]\n",
      "[6999.99, 1.40912301]\n",
      "[7000, 0.09851143]\n",
      "[7010, 0.06724219]\n",
      "[7050, 0.0107965]\n",
      "[7058.65, 0.1]\n",
      "[7064.99, 0.07726997]\n",
      "[7065, 0.17070588]\n",
      "[7089, 0.2]\n",
      "[7090, 0.8144629]\n",
      "[7100, 0.04425531]\n",
      "[7160, 0.00331086]\n",
      "[7166.99, 0.00231077]\n",
      "[7199.99, 0.05543645]\n",
      "[7219, 0.05564306]\n",
      "[7277.37, 0.16215604]\n",
      "[7290, 0.06250478]\n",
      "[7299.99, 0.05543645]\n",
      "[7370, 0.002]\n",
      "[7399.99, 0.05543645]\n",
      "[7400, 0.07352721]\n",
      "[7440, 0.5]\n",
      "[7450, 0.1468423]\n",
      "[7490, 0.006]\n",
      "[7499, 0.06961719]\n",
      "[7499.99, 0.05543645]\n",
      "[7500, 0.0477563]\n",
      "[7559, 0.00840681]\n",
      "[7560, 0.0335]\n",
      "[7599.99, 0.05543645]\n",
      "[7620, 0.002]\n",
      "[7699.99, 0.05543645]\n",
      "[7700, 0.01]\n",
      "[7701, 0.00087592]\n",
      "[7770, 0.002]\n",
      "[7799.99, 0.05543645]\n",
      "[7852.49, 0.00071315]\n",
      "[7899.99, 0.05543645]\n",
      "[7950, 0.04841154]\n",
      "[7970, 0.002]\n",
      "[7990, 0.02999998]\n",
      "[7999.5, 0.057]\n",
      "[7999.99, 0.05543645]\n",
      "[8000, 0.27650914]\n",
      "[8050, 0.22937022]\n",
      "buy\n",
      "[6705.94, 0.14521]\n",
      "[6705.93, 0.00368417]\n",
      "[6638, 0.01]\n",
      "[6620, 0.001]\n",
      "[6617, 0.02]\n",
      "[6600.01, 2.78465484]\n",
      "[6600, 0.06185303]\n",
      "[6570, 0.001]\n",
      "[6550, 0.08809618]\n",
      "[6520.01, 0.00424226]\n",
      "[6520, 0.001]\n",
      "[6500, 0.07400154]\n",
      "[6450, 0.02]\n",
      "[6407.71, 0.06894975]\n",
      "[6400, 0.09687656]\n",
      "[6300, 0.00791746]\n",
      "[6220, 0.001]\n",
      "[6200, 0.10798226]\n",
      "[6110, 0.01]\n",
      "[6100, 0.00709672]\n",
      "[6070.99, 0.10089788]\n",
      "[6010, 0.00781]\n",
      "[6000, 0.050985]\n",
      "[5980, 0.05029599]\n",
      "[5950, 0.004]\n",
      "[5920, 0.10212838]\n",
      "[5909.94, 0.03391574]\n",
      "[5900, 0.002]\n",
      "[5870, 0.02129472]\n",
      "[5850, 0.002]\n",
      "[5820, 0.002]\n",
      "[5801, 0.00150664]\n",
      "[5800, 0.05283276]\n",
      "[5778.55, 0.0078826]\n",
      "[5750, 0.03678609]\n",
      "[5723.94, 0.03001604]\n",
      "[5700, 0.0018]\n",
      "[5670, 0.002]\n",
      "[5601.55, 0.01248762]\n",
      "[5600, 3.24530892]\n",
      "[5570, 0.002]\n",
      "[5555, 0.01485869]\n",
      "[5505.55, 0.00158386]\n",
      "[5503, 0.00541886]\n",
      "[5500, 0.08480727]\n",
      "[5494.94, 0.02365995]\n",
      "[5420, 0.002]\n",
      "[5400, 0.009]\n",
      "[5320, 0.001]\n",
      "[5312.09, 0.10033716]\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "\n",
    "def orderbook_get(): \n",
    "    response = requests.get(\"https://bitbay.net/API/Public/BTCUSD/orderbook.json\")\n",
    "    return response.json()\n",
    "\n",
    "def orderbook():\n",
    "    order = orderbook_get()\n",
    "    sale = order['asks']\n",
    "    buy = order['bids']\n",
    "    \n",
    "    print ('sale')\n",
    "    \n",
    "    for i in range (50):\n",
    "        print(sale[i])\n",
    "        \n",
    "    print ('buy')\n",
    "    \n",
    "    for j in range (50):\n",
    "        print(buy[j])\n",
    "        \n",
    "orderbook()\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
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
