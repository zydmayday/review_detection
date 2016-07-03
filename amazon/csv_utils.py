import csv, codecs, cStringIO


import sys

# print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

    def next_without_unicode(self):
        return self.reader.next()

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':
    f = '/home/data/amazon/MProductReviewsLatest.csv'
    fw = '/home/data/amazon/unicode_reviews.csv'
    # f = '/home/data/amazon/zyd/MProductReviewsLatest_10.csv'
    # fw = '/home/data/amazon/zyd/unicodeReviews_10.csv'
    # ur = UnicodeReader(open(f))
    ur = open(f)
    # uw = UnicodeWriter(open(fw, 'w'))
    uw = open(fw, 'w')
    count = 0
    while 1:
        line = ''
        try:
            line = ur.readline()
            if line:
                uw.write(line.decode('utf-8'))
                count += 1
            else:
                break
        except UnicodeDecodeError:
            continue
    print count